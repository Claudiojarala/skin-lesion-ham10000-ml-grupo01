# Regenera el diagrama de flujo (Figura 2) (LANG_FIG=en|es)
import matplotlib, os; matplotlib.use("Agg")
ES=os.environ.get("LANG_FIG","en")=="es"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family":"DejaVu Sans"})
BLUE="#257de0"; ORANGE="#f47230"; INK="#191919"; GREY="#666666"
fig,ax=plt.subplots(figsize=(7.2,6.0)); ax.set_xlim(0,100); ax.set_ylim(0,84); ax.axis("off")
def box(x,y,w,h,txt,ec=GREY,fs=7.2,bold=False,lw=1.1):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.2,rounding_size=1.2",ec=ec,fc="white",lw=lw))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=INK,fontweight="bold" if bold else "normal",linespacing=1.3)
def arr(x1,y1,x2,y2,c=GREY):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=9,color=c,lw=1.1,shrinkA=0,shrinkB=0))
box(1,70,30,12,("HAM10000\n10,015 imágenes\n7,470 lesiones, 7 clases" if ES else "HAM10000\n10,015 images\n7,470 lesions, 7 classes"),bold=True)
box(35,70,30,12,("Preprocesamiento\nEliminación de vello (DullRazor)\nContraste AGCWD\n224×224, norm. ImageNet" if ES else "Preprocessing\nDullRazor hair removal\nAGCWD contrast\n224×224, ImageNet norm."))
box(69,70,30,12,("Cuatro redes congeladas\nResNet-50, DenseNet-201\nConvNeXt-Tiny, Swin-Tiny\n(características agrupadas)" if ES else "Four frozen backbones\nResNet-50, DenseNet-201\nConvNeXt-Tiny, Swin-Tiny\n(pooled features)"))
arr(31,76,35,76); arr(65,76,69,76)
box(12,55,76,10,("Primero, partición agrupada por lesión\n(StratifiedGroupKFold, 10 pliegues; 3 como prueba = 30 %)" if ES else "Lesion-grouped split first\n(StratifiedGroupKFold, 10 folds; 3 folds as test = 30 %)"),bold=True,fs=7.2)
arr(84,70,70,65.3)
box(1,41,56,11,("Entrenamiento: 6,985 imágenes (5,228 lesiones)\nCV interna agrupada de 5 pliegues elige C por F1 macro\nRemuestreo (escenario B) solo en pliegues de entrenamiento" if ES else "Training set: 6,985 images (5,228 lesions)\nInner grouped 5-fold CV selects C by macro-F1\nResampling (scenario B) only on training folds"),ec=INK,fs=6.7)
box(61,41,38,11,("Prueba: 3,030 imágenes (2,242 lesiones)\nno se usa para ajustar, afinar ni balancear" if ES else "Test set: 3,030 images (2,242 lesions)\nnot used for fitting, tuning or balancing"),ec=INK,fs=6.7)
arr(35,56,29,52.3); arr(65,56,80,52.3)
box(1,22,26,13,("Escenario A\nStandardScaler →\nLogisticRegression" if ES else "Scenario A\nStandardScaler →\nLogisticRegression"),ec=BLUE,lw=1.9)
box(30,22,27,13,("Escenario B\nStandardScaler → sub- /\nsobremuestreo a 1,000 por\nclase → LogisticRegression" if ES else "Scenario B\nStandardScaler → under- /\nover-sampling to 1,000 per\nclass → LogisticRegression"),ec=ORANGE,lw=1.9,fs=6.9)
arr(14,41,14,35.3,BLUE); arr(43,41,43,35.3,ORANGE)
box(1,3,98,13,("Evaluación de A y B en el mismo conjunto de prueba\nExactitud, exactitud balanceada, F1 macro, MCC, AUC; IC 95 % bootstrap por lesión;\npruebas exactas de McNemar con Holm; cinco semillas de partición; control con etiquetas permutadas" if ES else "Evaluation of A and B on the same test set\nAccuracy, balanced accuracy, macro-F1, MCC, AUC; 95 % lesion-bootstrap CIs;\nexact McNemar tests with Holm correction; five partition seeds; permuted-label control"),fs=7.0)
arr(14,22,14,16.3,BLUE); arr(43,22,43,16.3,ORANGE); arr(80,41,80,16.3)
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","figuras_"+("es" if ES else "en"),"fig_workflow.png"),dpi=300,bbox_inches="tight",pad_inches=0.05)
