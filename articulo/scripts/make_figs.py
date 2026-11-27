# Regenera las figuras 1, 3, 4 y 5 del artículo (LANG_FIG=en|es). Requiere meta_ham10000.csv (HAM_META).
import sys, os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
LANG=os.environ.get("LANG_FIG","en")
ES=LANG=="es"
X=lambda en,es: es if ES else en
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cms import CM
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.edgecolor":"#666666","axes.labelcolor":"#191919","text.color":"#191919","xtick.color":"#191919","ytick.color":"#191919"})
BLUE="#257de0"; ORANGE="#f47230"; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",f"figuras_{LANG}")+"/"; os.makedirs(OUT,exist_ok=True)
CLS=["akiec","bcc","bkl","df","mel","nv","vasc"]; LAB=[c.upper() for c in CLS]
meta=pd.read_csv(os.environ.get("HAM_META","meta_ham10000.csv"))
# Fig 1 exploration
fig,ax=plt.subplots(1,2,figsize=(7.2,2.9))
vc=meta.dx.value_counts()
ax[0].barh([c.upper() for c in vc.index][::-1],vc.values[::-1],color=BLUE,height=0.7)
for y,v in enumerate(vc.values[::-1]): ax[0].text(v+80,y,f"{v:,}",va="center",fontsize=8,color="#666666")
ax[0].set_xlim(0,8000); ax[0].set_xlabel(X("Images","Imágenes")); ax[0].set_title(X("(a) Class distribution","(a) Distribución por clase"),fontsize=9.5,loc="left")
k=meta.groupby("lesion_id").size().value_counts().sort_index()
ax[1].bar(k.index,k.values,color=BLUE,width=0.8); ax[1].set_yscale("log")
for x,v in zip(k.index,k.values): ax[1].text(x,v*1.12,f"{v:,}",ha="center",fontsize=8,color="#666666")
ax[1].set_xlabel(X("Images per lesion","Imágenes por lesión")); ax[1].set_ylabel(X("Lesions (log scale)","Lesiones (escala log)")); ax[1].set_ylim(1,2e4)
ax[1].set_title(X("(b) Lesion structure","(b) Estructura por lesión"),fontsize=9.5,loc="left")
for a in ax: a.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"fig1_exploration.png",dpi=300); plt.close()
print(k.to_dict())
# Fig 2/3 confusion matrices
cmap=LinearSegmentedColormap.from_list("b",["#ffffff","#257de0"])
mods=["ResNet-50","DenseNet-201","ConvNeXt-Tiny","Swin-Tiny"]
for scen,fn,tag in [("A_sin_balanceo","fig2_cm_scenarioA.png",X("Scenario A (no balancing)","Escenario A (sin balanceo)")),("B_sobremuestreo_train","fig3_cm_scenarioB.png",X("Scenario B (balancing inside training)","Escenario B (balanceo dentro del entrenamiento)"))]:
    fig,axs=plt.subplots(2,2,figsize=(7.2,6.6))
    for a,m in zip(axs.ravel(),mods):
        M=CM[(scen,m)]; R=M/M.sum(1,keepdims=True)
        a.imshow(R,cmap=cmap,vmin=0,vmax=1)
        for i in range(7):
            for j in range(7):
                a.text(j,i,str(M[i,j]),ha="center",va="center",fontsize=6.5,color="white" if R[i,j]>0.55 else "#191919")
        a.set_xticks(range(7)); a.set_yticks(range(7)); a.set_xticklabels(LAB,rotation=45,ha="right",fontsize=7); a.set_yticklabels(LAB,fontsize=7)
        a.set_title(m,fontsize=9); a.set_xlabel(X("Predicted class","Clase predicha"),fontsize=8); a.set_ylabel(X("True class","Clase real"),fontsize=8)
    fig.suptitle(tag+X("; cell shading = row-normalised proportion (recall)","; sombreado = proporción normalizada por fila (sensibilidad)"),fontsize=9)
    plt.tight_layout(rect=[0,0,1,0.97]); plt.savefig(OUT+fn,dpi=300); plt.close()
# Fig 4 F1 comparison with CI
ci=pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","resultados_finales","tablas","tabla_intervalos_confianza.csv")); ci=ci[ci.metrica=="f1_macro"]
fig,ax=plt.subplots(figsize=(6.6,3.2)); w=0.36; x=np.arange(4)
for off,sc,col,lab in [(-w/2-0.01,"A_sin_balanceo",BLUE,X("A: no balancing","A: sin balanceo")),(w/2+0.01,"B_sobremuestreo_train",ORANGE,X("B: balancing in training","B: balanceo en entrenamiento"))]:
    d=ci[ci.escenario==sc].set_index("modelo").loc[mods]
    ax.bar(x+off,d.estimado,w,color=col,label=lab,yerr=[d.estimado-d.ic95_inf,d.ic95_sup-d.estimado],error_kw=dict(ecolor="#191919",lw=1,capsize=3))
    for xi,v in zip(x+off,d.estimado): ax.text(xi,0.012,f"{v:.3f}",ha="center",fontsize=7.5,color="white",rotation=90,va="bottom")
b=ci[ci.escenario=="L_base"].estimado.iloc[0]
ax.axhline(b,color="#666666",ls="--",lw=1,label=X(f"Majority-class baseline ({b:.3f})",f"Línea base de clase mayoritaria ({b:.3f})"))
ax.set_xticks(x); ax.set_xticklabels(mods); ax.set_ylabel(X("Test macro-F1 (95% lesion-bootstrap CI)","F1 macro en prueba (IC 95 % bootstrap por lesión)")); ax.set_ylim(0,0.75)
ax.legend(frameon=False,fontsize=8,loc="upper left",ncol=3,columnspacing=1.2,handlelength=1.5); ax.spines[["top","right"]].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"fig4_f1_comparison.png",dpi=300); plt.close()
