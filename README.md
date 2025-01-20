# easySI
CN
大二学生的第一个项目，一个简单的同声传译程序
如何使用:
先从vosk官网下载三种语言模型：
https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
下载完成后，在目录里面创建一个model文件夹，把三个压缩包里面的同名文件夹，全部解压到model文件夹内
然后运行需要的语言的.py程序即可使用。
记得要使用voicemeeter来把电脑音频输出转换成输入，以便识别电脑音频，否则是识别麦克风音频！


EN
The first project of a sophomore student: an easy simultaneous interpretation program
How to use:
Download the three language models from Vosk:
https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
After downloading, create a "model" folder in your directory and extract the corresponding folders from each zip file into the "model" folder. Then, run the required language's Python script to use it.
Remember to use Voicemeeter to route the computer's audio output to input for recognition; otherwise, only microphone audio will be recognized!


RU
Первый проект студента второго курса — простая программа для синхронного перевода
Как использовать:
Скачайте три модели языка с сайта Vosk:
https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip
https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
После загрузки создайте папку "model" в вашем каталоге и извлеките папки с одинаковыми именами из каждого архива в эту папку
Запустите соответствующую программу .py для использования. Не забудьте использовать Voicemeeter для маршрутизации звука с компьютера в режим ввода для распознавания аудио с компьютера, иначе будет распознаваться только звук с микрофона!


最终树状图/Final Tree Diagram/Итоговая диаграмма дерева：
easySI
│
├── requirements.txt
├── model
│   ├── vosk-model-en-us-0.42-gigaspeech/
│   ├── vosk-model-cn-0.22/
│   └── vosk-model-ru-0.42/
├── gui_cn.py
├── gui_en.py
└── gui_ru.py

这个项目是由我的三脚猫功夫和GPT的共同努力下完成的，做出了可视化界面，本来还想让项目移植到其他人电脑上可以正常使用，但是用pyinstaller的时候会报错name 'DBAPIConnection' is not defined，所以放弃了，这次的项目作为一次练手，顺便熟悉一下github的上传功能。
This project was completed with the joint effort of my poor skills and GPT. A graphical user interface (GUI) was my final step. Originally, I intended to make the project portable so that it could be run on other people's computers, but I gave up when encountering an error (name 'DBAPIConnection' is not defined) during the use of PyInstaller. This project was treated as a learning exercise and an opportunity to get familiar with GitHub's upload functionality.
Этот проект был завершён совместными усилиями моих слабых навыков и GPT. Графический пользовательский интерфейс (GUI) стал моим финальным шагом. Изначально я хотел сделать проект портируемым, чтобы его можно было запустить на компьютерах других людей, но я сдался, столкнувшись с ошибкой (name 'DBAPIConnection' is not defined) при использовании PyInstaller. Этот проект был воспринят как упражнение для обучения и возможность ознакомиться с функциональностью загрузки на GitHub.
