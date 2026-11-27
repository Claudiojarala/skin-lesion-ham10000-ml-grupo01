# Clasificación de lesiones cutáneas (HAM10000) con cuatro arquitecturas preentrenadas

Código reproducible del manuscrito *Training, evaluation and comparison of machine learning architectures for the classification of dermatological conditions* (Grupo 01, curso Aprendizaje Automático I, Universidad San Ignacio de Loyola, Lima, Perú). Revista objetivo: *Bioengineering* (MDPI), ISSN 2306-5354.

**Autores:** Claudio Cronwell Jara Lamas, Bill Renzo Cornejo Condori y Alfredo Daza Vergaray (autor de correspondencia, alfredo.daza@usil.pe, ORCID 0000-0002-2259-1070).

## Qué compara
Cuatro extractores congelados preentrenados en ImageNet (ResNet-50, DenseNet-201, ConvNeXt-Tiny, Swin-Tiny) con regresión logística multinomial, bajo el **mismo protocolo**, sobre las 7 clases de HAM10000, con y sin equilibrado de clases.

## Protocolo sin fuga de datos
* Partición agrupada por `lesion_id` (`StratifiedGroupKFold`): ≈30 % de prueba (3 de 10 pliegues agrupados), que no se usa hasta la evaluación final. Primero se particiona y después se balancea.
* Validación cruzada agrupada de 5 pliegues y `GridSearchCV` solo sobre el entrenamiento.
* Escalado y remuestreo dentro del `Pipeline`, ajustados solo con el entrenamiento de cada pliegue.
* Ambos escenarios se evalúan sobre la **misma** prueba. Bootstrap por lesión (IC 95 %), McNemar con corrección de Holm, repetición con varias semillas y control con etiquetas permutadas.

## Datos
HAM10000, Tschandl, Rosendahl y Kittler (2018), *Scientific Data* 5:180161, https://doi.org/10.1038/sdata.2018.161  
Repositorio: Harvard Dataverse, https://doi.org/10.7910/DVN/DBW86T. **No se redistribuye aquí**; descargar `HAM10000_images_part_1.zip`, `HAM10000_images_part_2.zip` y `HAM10000_metadata`. Licencia indicada en el repositorio: CC BY-NC 4.0 (verificar en la página del dataset).

## Ejecución
1. Abrir `notebooks/Experimentos_Final_Grupo01.ipynb` en Google Colab con GPU (T4) y editar solo `BASE_DRIVE` en la celda de configuración.
2. **Parte A** (una vez, ~20–40 min): preprocesa cada imagen una vez y guarda los embeddings de las cuatro redes.
3. **Parte B** (CPU): partición, validación, evaluación, estadística y exportación a `resultados_finales/`.
4. Prueba rápida de humo: `N_SUBSET = 600` (no usar esas cifras en el artículo).

Las versiones de librerías usadas quedan registradas en `resultados_finales/entorno.json`. `TRAZABILIDAD.csv` indica qué sección del cuaderno genera cada tabla y figura del manuscrito.

## Estructura
```
notebooks/            cuaderno de experimentos
resultados_finales/   salidas del experimento final (tablas, figuras, trazabilidad, entorno)
docs/                 documentación de apoyo (matriz de correcciones)
requirements.txt
```

## Licencia
Código bajo licencia MIT (ver `LICENSE`). Los datos conservan la licencia de su fuente.
