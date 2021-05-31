# Тестовое задание BostonGene

Во вложении test_image_data.zip в папке tiled_data приведены изображения, полученные при съемке миндалин человека с помощью методики мультиплексной иммунофлюоресценции. Особенностью этого типа данных является довольно плотное расположение клеток.
Изображения сняты с перекрытием в 50% между каждым отснятым квадратом (назовём их тайлами), сторона тайла - 1024 пикселя (итого сетка 4 на 4 тайлов). Размерность снятого фрагмента ткани - квадрат со стороной 1548 пикселей. Папка tiled_data имеет подпапки, названные по имени маркеров, для детекции которых происходило окрашивание: DAPI - ядерный маркер, Ki67 - маркер делящихся популяций клеток, CD3e, CD4, CD8 - маркеры T-клеточных популяций, экспрессирующиеся на мембранах клеток, первый экспрессируется на всех Т-клетках в данном примере, два последних - маркеры субпопуляций T-клеток.
 В каждой из подпапок расположены тайлы в формате TIFF, индексация ведется с 1, тайлы были сняты последовательно строка за строкой, слева направо.


## Задания: 
1.	Необходимо провести сшивку (stitching) имеющихся тайлов для каждого из маркеров, получив таким образом полные изображения;
2.	Необходимо провести сегментацию отдельных клеток на данном фрагменте. Выбор технологии сегментации клеток свободный, можно использовать как трешхолдирование с вотершедом, так и иные методы на усмотрение. Protip: имеется набор мембранных маркеров, они могут помочь в процессе сегментации.
3.	На сшитом стеке видно, что не вся площадь отснятого слайда покрыта клетками, необходимо провести обрезку интересующего ROI автоматически.
4.	Полученные клетки можно охарактеризовать по среднему значению экспрессии в пределах ее сегмента. Нужно рассчитать средние значения экспрессии в сегментах и провести кластеризацию клеток по их видам. Затем вывести описательные статистики для набора данных: процентный состав кластеров, средняя величина интенсивности экспрессии маркеров в кластере, частоты контактов разных типов клеток в кластере. Набор статистик можно расширить по желанию, это будет являться плюсом при выполнении задачи.


Прим.:  Решение ожидается в виде архива репозитория git. При выполнении плюсом будет являться оформление в виде пайлпайна (прим. используя Snakemake или Nextflow, либо любой другой workflow engine на усмотрение), выполнение которого позволяет получить все результаты работы воспроизводимым образом. Для работы можно использовать ImageJ и скрипты на нем. Ход работы и расчет различных статистик для набора данных можно описывать в Jupyter Notebook или RMarkdown, при желании, можно оформить и в виде docx документа, в зависимости от удобства. При выполнении работы не обязательно делать каждый пункт “идеально”, главное последовательно описать каждый этап и почему были приняты те или иные решения при работе. Для невыполненных задач желательно объяснить причины и предположения, как их можно было бы решить при наличии большего времени.

# Workflow
1) Сшивка происходит внутри **1_Stitching.ipynb**, используя библиотеку OpenCV.
*Входные данные:* изображения внутри подпапок [] папки tiled_data, ряд папок игнорируется (это папки, сохраняющие результаты последующих этапов)
*Выходные данные:* изображения в формате pano_MarkerName.tif в папке tiled_data/Stitched
2) Обрезка ROI происходит в **3_ROI_cropping.ipynb**
*Входные данные:* {samples} из папки tiled_data/Stitched
*Выходные данные:* {samples} в папку tiled_data/Stitched_cropped
3) Предобработка полученных изображений проводится в **2.0_Preprocessing.ipynb**
*Входные данные:* {samples} из папки tiled_data/Stitched_cropped
*Выходные данные:* {samples} в папку tiled_data/Stitched_cropped_preprocessed
4) Сегментация ядер проводится в **2.1_Segmentation.ipynb**
*Входные данные:* изображение pano_DAPI.tif из папки tiled_data/Stitched_cropped_preprocessed
*Выходные данные:* бинарные маски в формате BW_nuclei_method в папку tiled_data\BW_nuclei
***и***
изображение канала DAPI с контурами масок в формате BW_nuclei_method в папку tiled_data\BW_nuclei_on_img
5) Разделение кластеров проводится в **2.2_Splitting_Clusters.ipynb**
*Входные данные:* сшитые обрезанные предобработанные изображения из папки tiled_data/Stitched_cropped_preprocessed и 
маски ядер из папки tiled_data\BW_nucle
*Выходные данные:* 200 изображений объектов для последующей классификации в папку tiled_data\BW_cluster_solo (далее изображения вручную были разнесены по подпапкам Solo и Cluster)
tiled_data\BW_cluster_solo\summary.csv - суммарная информация по признакам и меткам полученных объектов
tiled_data\BW_cluster_solo\BW_summary_Stardist_from_I_nuclei.tif - маска ядер с разбитыми кластерами с использованием алгоритма Stardist
6) Подсчет статистики произведен в **4_Statistics.ipynb**
*Входные данные:* обрезанные сшитые изображения каждого канала из папки tiled_data/Stitched_cropped
***и***
маска ядер tiled_data\BW_cluster_solo\BW_summary_Stardist_from_I_nuclei.tif
*Выходные данные:* Набор статистик внутри ноутбука (гистограммы, процентное соотношение клеток различных популяций, изображения с отображением клеток различных классов на нем, выборочное среднее и СКО нормированной интенсивности для клеток различных популяций, число контактов клеток различных классов между собой)