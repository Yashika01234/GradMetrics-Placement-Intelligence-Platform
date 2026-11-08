
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import csv,json,statistics
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"students.csv"
def load():
 with DATA.open(newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
 for r in rows:
  r["year"]=int(r["year"]);r["cgpa"]=float(r["cgpa"]);r["package_lpa"]=float(r["package_lpa"])
 return rows
def filt(rows,y=None,b=None):
 if y and y!="All": rows=[r for r in rows if r["year"]==int(y)]
 if b and b!="All": rows=[r for r in rows if r["branch"]==b]
 return rows
def summary(rows):
 n=len(rows);placed=[r for r in rows if r["status"]=="Placed"];pk=[r["package_lpa"] for r in placed if r["package_lpa"]>0]
 return {"students":n,"placed":len(placed),"not_placed":n-len(placed),"placement_rate":round(len(placed)*100/n,1) if n else 0,
 "avg_package":round(statistics.mean(pk),2) if pk else 0,"median_package":round(statistics.median(pk),2) if pk else 0,"highest_package":round(max(pk),2) if pk else 0}
def forecast(points):
 xs=[p[0] for p in points];ys=[p[1] for p in points]
 if len(xs)<2:return None
 xm=sum(xs)/len(xs);ym=sum(ys)/len(ys);den=sum((x-xm)**2 for x in xs)
 if not den:return None
 m=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den
 return round(max(0,min(100,ym+m*(max(xs)+1-xm))),1)
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/"static"),**kw)
 def log_message(self,*a):pass
 def sendj(self,o,status=200):
  d=json.dumps(o).encode();self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(d)));self.end_headers();self.wfile.write(d)
 def do_GET(self):
  u=urlparse(self.path)
  if not u.path.startswith("/api/"):return super().do_GET()
  q=parse_qs(u.query);allr=load();r=filt(allr,q.get("year",[None])[0],q.get("branch",[None])[0])
  if u.path=="/api/summary":
   bs=[]
   for b in sorted(set(x["branch"] for x in r)):bs.append({"branch":b,**summary([x for x in r if x["branch"]==b])})
   trend=[{"year":y,**{k:summary(filt(allr,str(y),q.get("branch",[None])[0]))[k] for k in ["placement_rate","placed","students"]}} for y in sorted(set(x["year"] for x in allr))]
   return self.sendj({"kpis":summary(r),"branches":bs,"trend":trend,"years":sorted(set(x["year"] for x in allr)),"branch_names":sorted(set(x["branch"] for x in allr))})
  if u.path=="/api/students":return self.sendj({"students":r[:3000]})
  if u.path=="/api/forecast":
   out=[]
   for b in sorted(set(x["branch"] for x in allr)):
    hist=[(y,summary(filt(allr,str(y),b))["placement_rate"]) for y in sorted(set(x["year"] for x in allr))]
    out.append({"branch":b,"forecast":forecast(hist),"history":[{"year":x,"rate":y} for x,y in hist]})
   return self.sendj({"forecasts":out})
  return self.sendj({"error":"Not found"},404)
 def do_POST(self):
  n=int(self.headers.get("Content-Length",0));p=json.loads(self.rfile.read(n) or b"{}")
  if self.path!="/api/scenario":return self.sendj({"error":"Not found"},404)
  total=max(1,int(p.get("total_students",1)));cur=int(p.get("current_placed",0));extra=min(max(0,int(p.get("additional_placements",0))),max(0,total-cur));new=cur+extra
  return self.sendj({"current_rate":round(cur/total*100,1),"projected_placed":new,"projected_rate":round(new/total*100,1),"rate_change":round(extra/total*100,1),"remaining_unplaced":total-new})
def main():
 print("\\nGradMetrics running: http://127.0.0.1:8000\\nPress Ctrl+C to stop.")
 ThreadingHTTPServer(("127.0.0.1",8000),H).serve_forever()
if __name__=="__main__":
 main()
