# Clasificación de lesiones cutáneas (HAM10000) con cuatro arquitecturas preentrenadas

Código reproducible del manuscrito *Lesion-Grouped Evaluation of Four Frozen Pretrained Architectures for Seven-Class Dermoscopic Skin Lesion Classification on HAM10000* (Grupo 01, curso Aprendizaje Automático I, Universidad San Ignacio de Loyola, Lima, Perú). Revista objetivo: *Bioengineering* (MDPI), ISSN 2306-5354.

**Autores:** Claudio Cronwell Jara Lamas, Bill Renzo Cornejo Condori y Alfredo Daza Vergaray (autor de correspondencia, alfredo.daza@usil.pe, ORCID 0000-0002-2259-1070).

## Qué compara
Cuatro extractores congelados preentrenados en ImageNet (ResNet-50, DenseNet-201, ConvNeXt-Tiny, Swin-Tiny) con regresión logística multinomial, bajo el **mismo protocolo**, sobre las 7 clases de HAM10000, con y sin equilibrado de clases.

## Protocolo sin fuga de datos
* Partición agrupada por `lesion_id` (`StratifiedGroupKFold`): ≈30 % de prueba (3 de 10 pliegues agrupados), que no se usa hasta la evaluación final. Primero se particiona y después se balancea.
* Validación cruzada agrupada de 5 pliegues y `GridSearchCV` solo sobre el entrenamiento.
* Escalado y remuestreo dentro del `Pipeline`, ajustados solo con el entrenamiento de cada pliegue.
* Ambos escenarios se evalúan sobre la **misma** prueba. Bootstrap por lesión (IC 95 %), McNemar con corrección de Holm, repetición con varias semillas y control con etiquetas permutadas.

## Resultados principales (prueba de 3 030 imágenes, semilla 42)
A = sin balanceo, B = balanceo dentro del pipeline de entrenamiento. Línea base de clase mayoritaria: F1 macro 0.114.

| Modelo | F1 macro (IC 95 %) A | F1 macro (IC 95 %) B | Exactitud bal. A → B |
|---|---|---|---|
| ResNet-50 | 0.513 (0.469–0.556) | 0.485 (0.447–0.522) | 0.472 → 0.546 |
| DenseNet-201 | 0.618 (0.576–0.656) | 0.589 (0.551–0.623) | 0.578 → 0.670 |
| ConvNeXt-Tiny | 0.555 (0.507–0.595) | 0.537 (0.503–0.570) | 0.507 → 0.639 |
| Swin-Tiny | 0.554 (0.513–0.599) | 0.526 (0.491–0.559) | 0.529 → 0.631 |

Todas las cifras del artículo provienen de `resultados_finales/tablas/`.

## Datos
HAM10000, Tschandl, Rosendahl y Kittler (2018), *Scientific Data* 5:180161, https://doi.org/10.1038/sdata.2018.161  
Repositorio: Harvard Dataverse, https://doi.org/10.7910/DVN/DBW86T. **No se redistribuye aquí**; descargar `HAM10000_images_part_1.zip`, `HAM10000_images_part_2.zip` y `HAM10000_metadata`. Licencia indicada en el repositorio: CC BY-NC 4.0 (verificar en la página del dataset).

## Ejecución
1. Abrir `notebooks/Experimentos_Final_Grupo01.ipynb` en Google Colab con GPU (T4) y editar solo `BASE_DRIVE` en la celda de configuración.
2. **Parte A** (una vez, ~20–40 min): preprocesa cada imagen una vez y guarda los embeddings de las cuatro redes.
3. **Parte B** (CPU): partición, validación, evaluación, estadística y exportación a `resultados_finales/`.
4. Prueba rápida de humo: `N_SUBSET = 600` (no usar esas cifras en el artículo).

Las versiones de librerías usadas quedan registradas en `resultados_finales/entorno.json`. `TRAZABILIDAD_manuscrito_final.csv` indica qué sección del cuaderno genera cada tabla y figura del manuscrito final (`TRAZABILIDAD.csv`, exportado por el cuaderno, conserva la numeración de un borrador anterior).

## Estructura
```
notebooks/            cuaderno de experimentos
resultados_finales/   salidas del experimento final (tablas, figuras, trazabilidad, entorno)
articulo/             figuras del artículo (en/es) y scripts que las regeneran
docs/                 manuscritos (ES/EN), anexo experimental, datos o acceso, ficha de revista, matriz de correcciones y declaraciones
requirements.txt
```
Nota: las matrices de confusión de `articulo/scripts/cms.py` se transcribieron de las figuras del cuaderno y se validaron contra la tabla de métricas por clase (`tabla_metricas_por_clase.csv`).

## Licencia
Código bajo licencia MIT (ver `LICENSE`). Los datos conservan la licencia de su fuente.
