# Selection-image Dataset

This dataset contains prompts that are designed to be used together with the images that are provided in the [images folder](images).

The first column contains the unique identifier of the file, the second the Parsee extraction template ID and the third the ID of the question (for more details about the questions, please check out our study).

The fourth column contains the expected answer of the model (which is JSON) and the fifth column the full prompt, that can directly be fed to a LLM.

In the last column is the page index that together with the first column can be used to find the relevant image needed for answering the question.

The image naming convention is as follows: {file_identifier}_p{page_index}.jpg

So for a file identifier "28cd6e976eb53b4f0a4af0d213609538967b325c1371966074b0ae74fbc14222"

and a page index of 55 (this is the first entry in the CSV file), the name of the image file is:

28cd6e976eb53b4f0a4af0d213609538967b325c1371966074b0ae74fbc14222_p55.jpg

This dataset contains a total of 3,468 rows, 1,130,591 tokens (counted with tiktoken cl100k_base) and 1,156 images.