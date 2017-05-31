# language_identifier
This project is aimed to creating a python program to identify tha language a document/text is written in without the use of any external libraries.

The implementation is done using Naive Bayes approach. The languages that the model is trained on are
```sh
French, English, Arabic, Russian, German, Italian, Greek, Spanish, Thai,
Persian, Chinese, Turkish, Finnish, Portuguese, Roman, Indonesian,
Polish, Dutch, Irish, Icelandic, Hindi, Czech, Malay, Bulgarian, Urdu,
Norwegian, Danish, Hebrew, Swedish, Hungarian, Latin, and Albanian
```

The train data used for the model training are the <a href = 'https://github.com/xprogramer/DLI32-corpus' target='_blank'>DLI32-corpus </a>

The DLI32 corpus contains 320 texts corresponding to 10 texts per language and DLI32-2 corpus consists of 640 texts corresponding to 0 texts per language.

#Running the program
To identify the language of a text sentence directly
>$ python language_identifier.py <text_sentence>

example :
>$ python language_identifier.py 'The weather here is awesome'

To identify the language for a number of sentences.
Save the sentences in a csv file delimited by ',' in the format
```sh
 <sentence>, <label>
```
then     
>$ python language_identifier.py <file_path>
