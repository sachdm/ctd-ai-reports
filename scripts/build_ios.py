from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import ParagraphStyle
BG=HexColor("#F2F2F7");CARD=HexColor("#FFFFFF");LABEL=HexColor("#1C1C1E");LABEL2=HexColor("#8A8A8E");LABEL3=HexColor("#AEAEB2")
SEP=HexColor("#E5E5EA");TRACK=HexColor("#E9E9EE");BLUE=HexColor("#0A84FF");GREEN=HexColor("#30B152");RED=HexColor("#FF3B30")
ORANGE=HexColor("#FF9500");PURPLE=HexColor("#5E5CE6");BLUET=HexColor("#EAF2FF");GREENT=HexColor("#EAF7EE");ORANGET=HexColor("#FFF4E5")
PGW,PGH=letter;M=0.82*inch;W=PGW-2*M
def PS(n,**k):
    b=dict(fontName="Helvetica",fontSize=10,leading=14.5,textColor=LABEL);b.update(k);return ParagraphStyle(n,**b)
eyebrow=PS("eb",fontName="Helvetica-Bold",fontSize=8,textColor=BLUE,leading=10)
h1=PS("h1",fontName="Helvetica-Bold",fontSize=25,leading=28,spaceAfter=3)
dek=PS("dek",fontSize=10.5,textColor=LABEL2,leading=15,spaceAfter=4)
sechdr=PS("s",fontName="Helvetica-Bold",fontSize=16,leading=19)
subhd=PS("sub",fontSize=9,textColor=LABEL2,leading=12.5,spaceAfter=6)
body=PS("body",fontSize=9.7,leading=14)
th=PS("th",fontName="Helvetica-Bold",fontSize=7,textColor=LABEL3,leading=9)
cell=PS("cell",fontSize=9.6,leading=13);cellb=PS("cellb",fontName="Helvetica-Bold",fontSize=11,leading=13)
kbig=PS("kb",fontName="Helvetica-Bold",fontSize=22,leading=23);klab=PS("kl",fontSize=7.6,textColor=LABEL2,leading=9.5)
class RBar(Flowable):
    def __init__(s,pct,color,width,height=7,track=TRACK):
        Flowable.__init__(s);s.pct=pct;s.color=color;s.width=width;s.height=height;s.track=track
    def wrap(s,*a):return(s.width,s.height)
    def draw(s):
        c=s.canv;r=s.height/2.0;c.setFillColor(s.track);c.roundRect(0,0,s.width,s.height,r,fill=1,stroke=0)
        fw=max(s.height,min(1.0,s.pct/100.0)*s.width);c.setFillColor(s.color);c.roundRect(0,0,fw,s.height,r,fill=1,stroke=0)
E=[]
def gap(h=6):E.append(Spacer(1,h))
def card(inner,bg=CARD,pad=13,radius=14,gapa=9):
    t=Table([[inner]],colWidths=[W]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("ROUNDEDCORNERS",[radius]*4),
        ("LEFTPADDING",(0,0),(-1,-1),pad),("RIGHTPADDING",(0,0),(-1,-1),pad),("TOPPADDING",(0,0),(-1,-1),pad-1),
        ("BOTTOMPADDING",(0,0),(-1,-1),pad-1)]));E.append(t);gap(gapa)
def group(header,rows,colw,radius=14):
    data=[[Paragraph(h,th) for h in header]]+rows;t=Table(data,colWidths=colw)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CARD),("ROUNDEDCORNERS",[radius]*4),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,0),9),("BOTTOMPADDING",(0,0),(-1,0),6),("TOPPADDING",(0,1),(-1,-1),8),("BOTTOMPADDING",(0,1),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),13),("RIGHTPADDING",(0,0),(-1,-1),13),("LINEBELOW",(0,1),(-1,-2),0.5,SEP)]));E.append(t);gap(9)
def barcell(txt,pct,color,w=1.0*inch,tc=None):
    tc=tc or LABEL
    return Table([[Paragraph(f"<font color='#{tc.hexval()[2:]}'>{txt}</font>",cellb)],[RBar(pct,color,w)]],colWidths=[w],
        style=[("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),
               ("BOTTOMPADDING",(0,0),(-1,0),2),("BOTTOMPADDING",(0,1),(-1,1),0)])
def sec(t):gap(6);E.append(Paragraph(t,sechdr));gap(2)
E.append(Paragraph("CLOSE TO DISASTER · GEN AI",eyebrow));gap(4)
E.append(Paragraph("The GEN AI Program,<br/>by the Numbers",h1));gap(1)
E.append(Paragraph("How much AI is in the cuts, how efficiently we&#39;re generating it, re-spin load, and where every shot stands. Read-only pull of the CTD Airtable · July 23, 2026.",dek));gap(8)
def kpi(num,lab,accent=LABEL):
    inner=[Paragraph(f"<font color='#{accent.hexval()[2:]}'>{num}</font>",kbig),Spacer(1,3),Paragraph(lab,klab)]
    t=Table([[inner]],colWidths=[(W-3*8)/4.0]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CARD),("ROUNDEDCORNERS",[13]*4),
        ("LEFTPADDING",(0,0),(-1,-1),11),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),11),
        ("BOTTOMPADDING",(0,0),(-1,-1),11),("VALIGN",(0,0),(-1,-1),"TOP")]));return t
krow=Table([[kpi("33%","of each episode is AI footage"),kpi("2.4:1","generate-to-use, from 5.1:1",GREEN),
             kpi("0.66","re-spins / delivered shot",BLUE),kpi("712","shots delivered to Cream")]],colWidths=[(W)/4.0]*4)
krow.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(2,-1),8),("RIGHTPADDING",(3,0),(3,-1),0),
    ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"TOP")]));E.append(krow);gap(10)
card([Paragraph("<b>In one sentence.</b>  Generative AI reliably fills about a third of every episode, we&#39;re producing it more than twice as efficiently as when we started, re-spin churn has more than halved since episode 101, and just over half of all planned shots are already delivered.",body)])
sec("AI in the cuts")
E.append(Paragraph("Screen-time share per cut. Runtime = the timeline position of each cut&#39;s final AI clip, so these are floors.",subhd))
def cr(name,tag,c,st,rt,pct):
    nm=Paragraph(f"{name} <font size=7 color='#8A8A8E'>{tag}</font>" if tag else name,cellb)
    return [nm,Paragraph(c,cell),Paragraph(st,cell),Paragraph(rt,cell),barcell(f"{pct:.0f}%",pct,BLUE,0.8*inch)]
group(["CUT","CLIPS","SCREEN-TIME","RUNTIME","AI SHARE"],
   [cr("101 Fine Cut","+snap-ins","368","14:23","43:36",33),cr("102 Rough Cut 1","","295","14:33","44:49",33),
    cr("103 Rough Cut","","318","12:02","43:12",28)],
   [1.7*inch,0.62*inch,1.02*inch,0.92*inch,1.36*inch])
card([Paragraph("<b>A structural third of the show.</b>  The share holds at ~28–33% across three cuts and doesn&#39;t shrink as a cut matures — 101&#39;s locked fine cut carries <i>more</i> AI than its own earlier rough cut. 103 is lower only because it&#39;s a first assembly.",body)],bg=BLUET)
sec("Efficiency — are we improving?")
E.append(Paragraph("Clips generated per clip that lands in the cut. Lower is leaner.",subhd))
def er(ep,g,u,r,pct,cl):return [Paragraph(ep,cellb),Paragraph(g,cell),Paragraph(u,cell),barcell(r,pct,cl,1.0*inch,cl)]
group(["EPISODE","GENERATED","IN CUT","GENERATE-TO-USE"],
   [er("101","1,879","368","5.1 : 1",100,RED),er("102","872","295","3.0 : 1",59,ORANGE),er("103","774","318","2.4 : 1",47,GREEN)],
   [1.5*inch,1.4*inch,1.2*inch,2.6*inch])
card([Paragraph("<b>Yes — sharply.</b>  The generate-to-use ratio has more than halved across three episodes: the same on-screen output for less than half the generation waste. Locked prompt library, reference-frame workflow, and re-spin discipline compounding.",body)],bg=GREENT)
sec("Production pipeline")
E.append(Paragraph("Every planned shot and every generated file, by status.",subhd))
def dot(c):return f"<font color='#{c.hexval()[2:]}'>●</font>"
def pr(label,c,count,pct,bcol):return [Paragraph(f"{dot(c)}  {label}",cell),Paragraph(count,cellb),barcell(f"{pct}%",pct,bcol,1.5*inch)]
group(["STAGE","COUNT","SHARE OF PLANNED SHOTS"],
   [pr("Sent to Cream",GREEN,"712",52,GREEN),pr("First request",BLUE,"106",8,BLUE),pr("In progress",ORANGE,"69",5,ORANGE),
    pr("Paused / unset",LABEL3,"493",35,LABEL3),
    [Paragraph("<b>Total planned shots</b>",cell),Paragraph("1,380",cellb),Paragraph("across all episodes",subhd)]],
   [1.9*inch,1.0*inch,3.7*inch])
group(["GENERATION","COUNT","NOTE"],
   [[Paragraph("Total clips generated",cell),Paragraph("3,990",cellb),Paragraph("~2.9 files per planned shot",subhd)],
    [Paragraph("Re-spin requests (all-time)",cell),Paragraph("522",cellb),Paragraph("~0.66 per delivered shot lately",subhd)],
    [Paragraph("Currently open re-spins",cell),Paragraph("142",cellb),Paragraph("rest re-spun and moved on",subhd)]],
   [2.5*inch,1.0*inch,3.1*inch])
sec("Re-spins")
E.append(Paragraph("Delivered clips sent back for changes, measured against SHOTS DELIVERED — you can only re-spin something you delivered, and a generated-file denominator just rewards over-generation. Re-spin passes per shot sent to Cream.",subhd))
def rr(ep,rs,dl,val,pct,cl):return [Paragraph(ep,cellb),Paragraph(rs,cell),Paragraph(dl,cell),barcell(val,pct,cl,1.0*inch,cl)]
group(["EPISODE","RE-SPINS","DELIVERED","RE-SPINS / DELIVERED SHOT"],
   [rr("101","251","159","1.58",100,RED),rr("102","110","167","0.66",42,GREEN),rr("103","145","220","0.66",42,GREEN),
    [Paragraph("<b>101–103</b>",cell),Paragraph("506",cellb),Paragraph("546",cell),Paragraph("<b>0.93</b>",cellb)]],
   [1.25*inch,1.35*inch,1.35*inch,2.45*inch])
def sr(story,ep,n,pct):return [Paragraph(story,cellb),Paragraph(ep,cell),Paragraph(n,cell),RBar(pct,PURPLE,1.7*inch)]
group(["STORY · HEAVIEST RE-SPIN LOAD","EP","RE-SPINS",""],
   [sr("FDN — Fukushima","101","71",100),sr("447 — Air France 447","101","64",90),sr("HMB — Halifax","103","47",66),
    sr("CHF / TXC (tie)","101","34",48),sr("SDS — Sampoong","103","31",44),sr("MSH — Mount St. Helens","101","29",41),
    sr("CCS — Costa Concordia","103","27",38)],
   [2.1*inch,0.6*inch,0.9*inch,2.2*inch])
card([Paragraph("<b>101 was the learning episode; 102 and 103 have settled.</b>  Churn ran 1.58 re-spin passes per delivered shot on 101 — the most rework while the pipeline was still finding its locks — then dropped to a flat 0.66 on both later episodes, less than half. Down and consistent, tracking the efficiency gain. FDN and 447 stay heaviest — effects-dense reactor and mid-air sequences where physics takes the most passes.",body)],bg=BLUET)
sec("By episode")
E.append(Paragraph("Everything lined up. Cut figures exist only where a cut is assembled (101–103).",subhd))
def epr(e,st,sh,g,r,rc,rs):
    return [Paragraph(e,cellb),Paragraph(st,cell),Paragraph(sh,cellb),Paragraph(g,cell),
            Paragraph(f"<font color='#{rc.hexval()[2:]}'><b>{r}</b></font>",cell) if r else Paragraph("—",subhd),Paragraph(rs,cell)]
group(["EP","CUT STAGE","AI SHARE","GEN.","GEN-TO-USE","RE-SPIN/SHOT"],
   [epr("101","Fine Cut","33%","1,879","5.1:1",RED,"1.58"),epr("102","Rough Cut 1","33%","872","3.0:1",ORANGE,"0.66"),
    epr("103","Rough Cut","28%","774","2.4:1",GREEN,"0.66"),
    [Paragraph("104",cellb),Paragraph("Not assembled",cell),Paragraph("—",subhd),Paragraph("",subhd),
       Paragraph("<i>first-request heavy: MVE, TSF, MRB</i>",subhd),Paragraph("",subhd)],
    [Paragraph("105",cellb),Paragraph("Not assembled",cell),Paragraph("—",subhd),Paragraph("",subhd),
       Paragraph("<i>first-request heavy: HSA, QIS</i>",subhd),Paragraph("",subhd)]],
   [0.5*inch,1.35*inch,0.85*inch,0.8*inch,1.7*inch,1.06*inch])
card([Paragraph("<b>Where the risk is.</b>  104 and 105 carry the bulk of untouched first-request work and have no cut yet, so their AI share, efficiency and churn are unknown. If the curves hold they should run leaner than 101 — the numbers to watch.",body)],bg=ORANGET)
sec("Method & sources")
m=("<b>AI share</b>  ·  AI clip durations per cut (GEN AI REPORTS) minus outdated/duplicate, over runtime from each cut&#39;s final Seq-Out timecode.<br/><br/>"
   "<b>Efficiency</b>  ·  delivered files per episode&#39;s stories (GEN AI ASSETS) ÷ AI placements in that cut.<br/><br/>"
   "<b>Re-spins</b>  ·  files with a re-spin note, per story, over shots at Sent-to-Cream status per episode.<br/><br/>"
   "<b>Scope</b>  ·  1,523 clip placements · 3,990 generated files · 522 re-spin requests · 546 delivered shots (101–103) · 1,380 planned shots. Runtime and placements-as-clips are floors.")
card([Paragraph(m,PS("m",fontSize=9.2,leading=13.5))])
gap(6)
E.append(Paragraph("Compiled read-only — nothing written to the base.  Sources: GEN AI REPORTS · ASSETS · SHOTCODES.  July 23, 2026.",PS("f",fontSize=8,textColor=LABEL3)))
def paint_bg(c,d):
    c.saveState();c.setFillColor(BG);c.rect(0,0,PGW,PGH,fill=1,stroke=0);c.restoreState()
import os
OUT=os.environ.get("CTD_PDF_OUT",os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","reports","CTD_AI_Master_Report.pdf"))
os.makedirs(os.path.dirname(OUT),exist_ok=True)
doc=SimpleDocTemplate(OUT,pagesize=letter,
    leftMargin=M,rightMargin=M,topMargin=0.7*inch,bottomMargin=0.6*inch,title="CTD — GEN AI Master Report")
doc.build(E,onFirstPage=paint_bg,onLaterPages=paint_bg)
print("built")
