## How to use this package for QA

### Steps involved in QA/QC (when doing Manually)
1. Scraping the data
2. Annotating the data
3. Labeling the data
4. Getting results from Model into .csv file
5. Evaluating the model.

### This Package will help you to do all the above steps automatically.

## 1. clone the repository:

`https://github.com/mirfan-ahmad/ML-Models-QC.git`

## 2. How to install the dependencies:

`pip install -r requirements.txt`

## 3. How to Scrape the data from google_images?
### Navigate to the scripts directory

`python google_images.py "search query" limit <output-directory>`

```bash
If desired images couldn't be found in Google Images, write your own scraper or try to clone my following repository <if your desired website already scraped>

Note: This script will download the images from Google and also save the links of the images in links.txt file as well.
```
**Clone-Repository:** `https://github.com/mirfan-ahmad/Scraping.git`

```bash
Either using above scrapers or try to write your own scraper which will only scrape the links of the images and store them into text file in following format:
links1\n
links2\n
.
.
.
linkN
```

## 4. How to Download the images using links you have scraped?

`python download_images_via_link.py <txt_filename> <output-dir>`

## 5. How to annotate the data?

**annotate_data** `python annotate.py <img_dir>`

### How annotation will work?
```bash
1. After executing above command, it prompts the number of classes
2. It will iterate "number_of_classes" times to create seperate folders, Now the whole data has been classified into seperate folders.

Input Format:
Enter folder name: (Here you will enter the name of class to be classified)
Do you want to create a new folder (y/n)? (y: if you want to add more, n: No)

It will ask untill you enter 'n'

3. Once you enter 'n' It will gives you the instruction in terminal to assign given image to specific class.

e.g: 
Press -1- to choose <class1>   # class: name of folder
Press -2- to choose <class2>
.
.
Press -N- to choose <classN>

4. Suddenly, 1 by 1 images will be open and you just have to enter the key=1 or 2 .. N
5. As you click the key the image will be copied to integrated folder, and image will w8 until you enter 'q'
6. After you click the 'q' button, current image will be closed and next will be shown.

In this way all the images will be copied to integrated folder and classified into seperate folders.
```

## 6. How to create true labels?
### Navigate to the scripts directory

**If 1 folder**:<br>`python create_true_labels.py <img_dir> <storage> <annotated_img>`<br>
**If >1 folder**:<br>`python create_true_labels.py <img_dir1> <storage> <annotated_img1> .... <annotated_imgN>`

## 7. How to Get Results from Model deployed on cloud only?

**Command**:<br>
`python get_model_result.py <endpoint> <"[classes_names]"> <img_dir> <output_dir> <optional Parameters>`

```bash
Example-command:
python get_model_result.py endpoint "['signs', 'signs_date', 'text_name', 'text_address', 'text_date', 'text_company', 'text_phone_number', 'text_email']" /Input_dir/Images_links.txt output_dir url=True
OR
python get_model_result.py endpoint "['signs', 'signs_date', 'text_name', 'text_address', 'text_date', 'text_company', 'text_phone_number', 'text_email']" https://img.freepik.com/free-photo/cute-animals-group-white-background_23-2150038558.jpg output_dir url=True single_img=True
```
Let's know what above paramaters are:<br>
|<b>Parametes |<b>Usage|
|:---------------------------|:--------------------------|
|img_dir      |Input Image_dir Path              |
|output_dir   |Path to output directory          |
|endpoint     |endpoint of deployed model             |
|classes_names|name of classes you want to check weather the model is detecting or not<br>Format : "['class1', 'class2', ... , 'classN']"

<b>Optional Parameters (Fale: by_default):</b>
|<b>Parameters|<b>Usage|
|:---------------------------|:--------------------------|
|url|url=True, If you have links of images.
|model_name|enter model_name if you want to run any specific model
|reponse|if you want to get reponse from model|
|single_img|if you want to get result on single image|
|generative|generative=True<br>If you want to get the result as image from <br>Generative Models either masks or images

Note: parameters case-sensitivity shouldn't be undermined


## 8. How to Evaluate the Model?
### Navigate to the script directory

**Evaluate**: <br>`python evaluation.py <true_labels> <true_attribute> <predicted_labels> <predicted_attribute> <matrix_name>`

Let's know what above paramaters are:<br>

|<b>Parametes|<b>Usage|
|:---------------------------|:--------------------------|
|true_labels|true_labels.csv|
|true_attributes|list of true attributes|
|predicted_labels|predicted_labels.csv|
|predicted_attributes|list of predicted attributes|
|matrix_name|name of the matrix (e.g:text-watermark)|

Note: parameters case-sensitivity shouldn't be undermined

