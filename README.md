# How to run the code

​	After unpacking the two code packs, we need to run the front end and back end on WebStorm/VS Code and PyCharm respectively.

## Run the front-end code

First,we should open the terminal and run:

```shell
npm install
```

then, run

```sh
craco start
```

then the front end is running.

Then we can see the web page running in the browser

## Run the back-end code

First, create a new virtual environment. Make sure the the version of python is `python3.7.13`

then, install the relating packages and dependencies listed in `setup.py`

Then, run `rest-server.py`，then dependencies mainly includes:

```python
from setuptools import setup, find_packages

setup(
    name="speechmetrics",
    version="1.0",
    packages=find_packages(),

    install_requires=[
        'numpy',
        'scipy',
        'tqdm',
        'resampy',
        'pystoi',
        'museval',
        # This is requred, but srmrpy pull it in,
	    # and there is a pip3 conflict if we have the following
	    # line.
        #'gammatone @ git+https://github.com/detly/gammatone',
        'pypesq @ git+https://github.com/vBaiCai/python-pesq',
        'srmrpy @ git+https://github.com/jfsantos/SRMRpy',
        'pesq @ git+https://github.com/ludlows/python-pesq',
    ],
    extras_require={
        'cpu': ['tensorflow>=2.0.0', 'librosa'],
        'gpu': ['tensorflow-gpu>=2.0.0', 'librosa'],
    },
    include_package_data=True
)

```

If some packages on Github cannot be installed through `pip install`, you can download the corresponding ZIP and install locally

# Audio Quality Evaluation System

| Student Name | Student ID |
| ------------ | ---------- |
| Zhengyi Zhuo | 1850384    |
| Qiao Liang   | 1853572    |
| Kaixin Chen  | 1951724    |



## 1 Front-end Design & implementation

### 1.1 Design Decisions

We chose to use React and Material UI to implement the front-end side of or sound quality analysis application. Upon which, we add sound recording, internationalization, data visulization to enhance the user exprience. A brief dependency list will well describe this application's ability:

- `React` - For building the web page.
- `Material UI` - For basic user interface building, including themes and interactions.
- `i18next` - For easier i18n.
- `Echarts for React` - For sound quality result displaying.
- `recorder-js` - For on-page sound recording.
- `react-markdown` - For rendering markdown descriptions about our algorithms.
- `wavesurfer.js` - For audio visualization.

### 1.2 Package Structure

```
.
├── App.js                        # init
├── assets                        # images and static files
│   ├── bsseval.png
│   ├── mosnet.png
│   ├── pesq.png
│   ├── popup.css
│   ├── sisdr.png
│   ├── srmr.png
│   ├── stoi.png
│   └── videoplayback.mp4
├── components                  # Page Components
│   ├── AlgorithmSelection.js     # A checkbox group selecting algorithms
│   ├── AppBar.js                 # Bar on top
│   ├── PopUpCard.js              # Pop up description about algorithm
│   ├── RecorderController.js     # Timer and recording button for record
│   ├── SoundDenoiseResult.js     # Denoising result (showing an audio)
│   ├── SoundQualityResult.js     # SQA results (charts and figures)
│   ├── TabBar.js                 # Bar to bottom
│   ├── UploadController.js       # For uploading local file
│   ├── VideoCard.js              # Video of home page
│   └── WaveGraph.js              # Audio visualization
├── i18n                        # i18n text files
│   ├── en
│   │   └── main_en.json
│   └── zh
│       └── main_zh.json
├── i18n.js                     # i18n framwork init
├── index.js
├── pages                       # Higher level components
│   ├── Denoise.js                # Denoisng page
│   ├── Intro.js                  # Home page
│   ├── Layout.js                 # Overall layout
│   └── UploadOrRecord.js         # SQA page
├── requests                    # For API requesting
│   ├── audioDenoise.js
│   └── soundQuality.js
├── theme                       # theming related
│   ├── colorModification.js    
│   └── themeColor.js
└── utils                       # For time prettify
    └── format-time.js
```

### 1.3 Implementation Details

#### 1.3.1 On-Page Voice Recording

We used `Recorder.js` to aquire the browser's media control and managed to save the recorded sound clip into the form of `.wav`. The tough part is how the audio clip can be transformed from the original format into `.wav` so that the back-end can read the audio sequence without glitches. First we used the built in `MediaRecorder`(required by W3C standard) to record sounds. However there are still bugs un-resolved in this functionality that the `webm` form audio clip produced in this way has no duration field. That makes other software(except for Chromium browsers) hard to read this data sequence. Thus we found the encapsulated package `Recorder.js` , which helped overwrite the audio sequence format and easily produces `.wav` form audio clip file.
The following are the related codes:

```js
audioContext =  new (window.AudioContext || window.webkitAudioContext)();  
  
recorder = new Recorder(audioContext);

function start() {  
  recorder.start()  
      .then(() => {  
        setIsRecording(true);  
        setTimerInterval(setInterval(() => updateTime(), 1000))  
      });  
}

function saveRecording() {  
  console.log("Stopped recording")  
  recorder.stop()  
      .then(({blob, buffer}) => {  
        clearTime()  
        setAudioBlob(blob)  
        setIsRecording(false)  
        console.log(blob)  
        setGlobalAudio(window.URL.createObjectURL(blob))  
        // Recorder.download(blob, 'my-audio-file');  
        // buffer is an AudioBuffer      
    });  
}

function cancelRecording() {  
  console.log("Canceled recording")  
  recorder.stop();  
  setAudioBlob(null);  
  setIsRecording(false);  
  clearTime()  
}
```

#### 1.3.2 Audio Visulization

We chose to use `wavesurfer.js` to help transfor an audio `Blob` into graphic form. This is very useful when user wants to see how well the audio denoising function works. The component takes an `<audio>` tag or an audio `Blob` as input, we used the former one. The encapsulation is rather tight so we need not do more things concerning graphics displaying, but we still need to initialize the `WaveSurfer` and configure it to react to the interactions such as play / stop and rendering. The complete code can be found in file `WaveGraph.js`.

#### 1.3.3 Data Display and Visualization

`Echarts.js` is a very handy and popular tool for data disply in fron-end area, but we still took some time to figure out how to fill the `option` object so that the returned data from the back-end is properly shown in the page. Moreover, we found that `Echart.js` is not as powerful as `ploty.js` in scientific data displaying. Given another chance to refine our project, we would choose the latter for a possibly better solution.
The related code can be found in `SoundQualityResult.js`.

#### 1.3.4 Fully Internationalization

For i18n, we used an handy framework and the outcome is satisfying. `i18next` let us write all i18n related text into a `json` configuration file and load them during runtime. That helps us write the text phrases and easily decompose the language and text from the program code itself. The basics of `i18next` with `React` framework is a hook function:

```js
const {t} = useTranslation("main");
```

Later, with calling of the translating function `t`, the proper text will be injected into the specified places.

```js
const mdMap={  
    "mosnet":t("algo_md_info.mosnet"),  
    "srmr":t("algo_md_info.srmr"),  
    "bsseval":t("algo_md_info.bsseval"),  
    "pesq":t("algo_md_info.pesq"),  
    "sisdr":t("algo_md_info.sisdr"),  
    "stoi":t("algo_md_info.stoi"),  
}
```

- ## 3 structures and modules of Back-end

- ### 3.1 The backend architecture

​	Our project back end use `flask`  for realizing the back-end service, at the same time use `tensorflow2.3.0`, `tqdm`, `resampy`, `pystoi`, `museval` library retrieval back-end algorithm, etc.

​	Flask uses restful apis to call background algorithms for audio quality evaluation and audio noise reduction.

​	We mainly implemented the following two apis：

| URL                    | Method | Params                        | Description                                                  | Return example                                               |
| ---------------------- | ------ | ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| BASEURL/audioQuality   | POST   | Algorithms: array audio: blob | The input audio file and algorithm return the index score and algorithm running time of the corresponding algorithm evaluation | {                              "mosnet": {                  "avgScore": 2.9970579147338867,        "score": [            3.083199977874756,            2.9672365188598633,            3.211167335510254,            2.726627826690674        ],        "time": 2750    }                    } |
| BASEURL/audioDenoising | POST   | Audio:blob                    | Pass in the audio blob file to be de-noised and return the de-noised audio file | {'audio':blob}                                               |

### 3.2 back-end project structure

The back-end Flask project file structure is as follows：

.

├── LICENSE

├── MANIFEST.in

├── README.md

├── Server

│  ├── rest-server.py

│  └── templates

│    └── main.html

├── algorithm

│  ├── data

│  │  └── readme.txt

│  └── speechAssessment.py

├── ffmpeg.exe

├── requirements.txt

├── setup.py

└── speechmetrics

  ├── __init__.py

  ├── __pycache__

  │  └── __init__.cpython-37.pyc

  ├── absolute

  │  ├── __init__.py

  │  ├── __pycache__

  │  │  └── __init__.cpython-37.pyc

  │  ├── mosnet

  │  │  ├── __init__.py

  │  │  ├── __pycache__

  │  │  │  ├── __init__.cpython-37.pyc

  │  │  │  └── model.cpython-37.pyc

  │  │  ├── cnn_blstm.h5

  │  │  └── model.py

  │  └── srmr

  │    ├── LICENSE.md

  │    ├── __init__.py

  │    ├── __pycache__

  │    │  ├── __init__.cpython-37.pyc

  │    │  ├── hilbert.cpython-37.pyc

  │    │  ├── modulation_filters.cpython-37.pyc

  │    │  ├── segmentaxis.cpython-37.pyc

  │    │  ├── srmr.cpython-37.pyc

  │    │  └── vad.cpython-37.pyc

  │    ├── hilbert.py

  │    ├── modulation_filters.py

  │    ├── segmentaxis.py

  │    ├── srmr.py

  │    └── vad.py

  └── relative

​    ├── __init__.py

​    ├── __pycache__

​    │  ├── __init__.cpython-37.pyc

​    │  ├── bsseval.cpython-37.pyc

​    │  ├── pesq.cpython-37.pyc

​    │  ├── sisdr.cpython-37.pyc

​    │  └── stoi.cpython-37.pyc

​    ├── bsseval.py

​    ├── pesq.py

​    ├── sisdr.py

​    └── stoi.py

The following describes the functions of important files：

| File name           | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Rest-server.py      | Flask main entry, containing API implementation              |
| speechAssessment.py | Algorithm main file, algorithm API implementation, call each algorithm |
| algorithm           | Algorithm folder, the connotation of six folders of the recurrence code |
| cnn_blstm.h5        | Deep learning algorithm MOSNET model training file           |



### 3.3 Part of introduction of Algorithms

#### 3.3.1 PESQ

PESQ is a proxy for non-deep learning audio quality evaluation.

Audio quality evaluation algorithms can be roughly divided into the following two categories.

1. Intrusive algorithm
2. Non - intrusive algorithm

​	PESQ is an **intrusive** audio quality evaluation algorithm. Intrusive means that the algorithm needs to use the noiseless standard audio of the audio as a reference, and obtain the quality of the input audio by comparing the frequency spectrum. This is where the limits of invasive algorithms lie.

​	The result index of PESQ algorithm is the well-known MOS index. The MOS metric uses a score of 0-5 to indicate audio quality. The higher the score, the better the audio quality.

​	The following are the criteria for MOS indicators：

| Audio Level | Evaluation Standand                                  | Corresponding MOS |
| ----------- | ---------------------------------------------------- | ----------------- |
| A           | clear and sound; low delay, fluent communication     | 4.0-5.0           |
| B           | clear; low delay but with mild blocking and noise    | 3.5-4.0           |
| C           | Slightly unclear；Have delay but okay to communicate | 3.0-3.5           |
| D           | Unclear；Severe delay and requires repetition        | 1.5-3.0           |
| E           | Unrecognizable；Severe delay with blocking           | 0-1.5             |

​	PESQ, as described in the standard, can carry out end-to-end audio quality testing, the reference signal (Reference speech) line in passed into the transmitter (the following figure is a telephone), after the telephone network to the receiving end, and then Line out passed out and directly back to the loop (Figure called the reference path Reference path) of the reference signal passed into the PESQ The algorithm proceeds, with reference evaluation, and finally generates the PESQ score.

A simple PESQ algorithm is as follow：

![v2-a133189ac2149596495439e1a4a2bc8c_1440w](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/v2-a133189ac2149596495439e1a4a2bc8c_1440w-20220619233038292-20220619234316833.jpg)

​	In brief, the time Alignment detects the input active speech segment, then performs the delay calculation and speech segmentation, and this algorithm is compatible with variable delays. Then the PESQ Algorithm calculates the aligned reference signal and the signal to be measured, gets their signals in the frequency domain with some compensation, and then transfers them to the loudness domain to compare the perceptual differences between the two signals according to the psychoacoustic model. Finally, the difference is mapped to a PESQ score similar to the MOS score, which ranges from -0.5 to 4.5.



#### 3.3.2 Mosnet

https://doi.org/10.48550/arXiv.1904.08352

​	Unlike PESQ, MOSnet uses deep learning algorithms to achieve non-Intrusive audio quality evaluation that is closer to human subjective ratings. In this algorithm, CNN-BLSTM is used as a deep learning network. Because the BLSTM has the characteristics of anterior-posterior correlation, it can integrate the before and after frame information of audio, making the frame evaluation of audio quality more accurate. It also integrates the advantages of convolutional neural network.

![截屏2022-06-17 17.00.38](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.00.38-20220619234317050.png)

​	The model uses the data set shown above, which contains people's ratings of the audio conversion results, a natural audio quality corpus.

​	This paper proposes an objective evaluation method based on deep learning, which uses MOS to model human perception, called MOSNet. With the original amplitude spectrum as the input features and three new values, l network-based models, namely CNN, BLSTM and CNN-BLSTM, were used to extract valuable features from the input features of the fully connected (FC) layer to generate the predicted MOS. In the following sections, we'll look at each MOSNet component in detail. Using the extracted features, we use two FC layers to regression the frame-level features into a frame-level scalar to represent the naturalness score of each frame. Finally, a global averaging operation is where the application cheats the frame-level score to obtain the speech-level natural score.

![截屏2022-06-17 17.16.30](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.16.30-20220619234317273.png)

​	This algorithm uses a loss function based on mean square error, so the results are mostly clustered between 2.5-3.5 points, presenting a Gaussian distribution.

#### 3.3.3 SRMR

The speech-to-reverberation modulation energy ratio (SRMR) is a non-intrusive metric for speech quality and intelligibility based on a modulation spectral representation of the speech signal. The metric was proposed by Falk et al. and recently updated for variability reduction and improved intelligibility estimation both for normal hearing listeners and cochlear implant users

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/Snipaste_2022-06-15_21-17-34-20220619233038897-20220619234317330.png" alt="Snipaste_2022-06-15_21-17-34" style="zoom:67%;" />

In order to reduce this difference,The SRMR thresholding will be calculated. The objective is to truncate extremely low energies, which lead to high ratios due to the division done in SRMR, and also limit the modulation energy dynamic range. In our modulation energy limitation scheme, we first compute the energy values for each of the acoustic and modulation frequencies in all frames, and then compute the average peak value.
$$
\bar{E}_{p e a k}=\max _{j, f_{b}}\left(\frac{1}{M} \sum_{m=1}^{M} E_{j}\left(m, f_{b}\right)\right)
$$

The average peak will be use as an upper threshold of the modulation energy in each band for all frames. Finally an lower bound will be manually set to truncate the extremely low energies.

#### 3.3.4 Bsseval

BSS Eval is a Matlab toolbox to measure the performance of (blind) source separation algorithms within an evaluation framework where the original source signals are available as ground truth [1,3. The measures are based on the decomposition of each estimated source signal into a number of contributions corresponding to the target source, interference from unwanted sources, and artifacts such as "musical noise". They are valid for any type of data (audio, biomedical, etc), any mixture (instantaneous, convolutive, etc) and any algorithm (beamforming, ICA, time-frequency masking, etc). By separating the audio we get: 



$$
\widehat{s}_{j}=s_{\text {target }}+e_{\text {interf }}+e_{\text {noise }}+e_{\text {artif }}
$$
The seperation result contains target, interference, noise and artifacts. For a good seperation audio, the first 3 metric values should be 0. The alogritm of the individual algorithm is:



$$
\
\begin{aligned}
s_{\text {target }} &:=P_{s_{j}} \widehat{s}_{j} \\
e_{\text {interf }} &:=P_{\mathbf{s}} \widehat{s}_{j}-P_{s_{j}} \widehat{s}_{j} \\
e_{\text {noise }} &:=P_{\mathbf{s}, \mathbf{n}} \widehat{s}_{j}-P_{\mathbf{s}} \widehat{s}_{j} \\
e_{\text {artif }} &:=\widehat{s}_{j}-P_{\mathbf{s}, \mathbf{n}} \widehat{s}_{j}
\end{aligned}
$$



which can be simply represented with vector diagram:

#### 3.3.5 SISDR 

​	SISDR is a scale-invariant SDR(SISDR) algorithm based on SDR(signal distortion ratio). The algorithm uses the following formula to calculate SNR. The relationship between SNR and SI-SDR is shown below.

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.00.02-20220619234317387.png" alt="截屏2022-06-18 12.00.02" style="zoom:50%;" />

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2011.59.06-20220619233039302-20220619234317505.png" alt="截屏2022-06-18 11.59.06" style="zoom:50%;" />

​	To ensure that the residual is indeed orthogonal to the target, we can either rescale the target or rescale the estimate. Rescaling the target such that the residual is orthogonal to it corresponds to fifinding the orthogonal projection of the estimate *s*ˆ on the line spanned by the

target *s*, or equivalently fifinding the closest point to *s*ˆ along that line.This leads to two equivalent defifinitions for what we call the scale invariant signal-to-distortion ratio (SDR):

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.02.04-20220619234317665.png" alt="截屏2022-06-18 12.02.04" style="zoom:50%;" />

下图直观显示了SISDR和SDR的对比：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.04.19-20220619234317978.png" alt="截屏2022-06-18 12.04.19" style="zoom:50%;" />

#### 3.3.6 STOI

Paper addresses： https://ieeexplore.ieee.org/abstract/document/5495701

​	The algorithm presents an objective solvability measure, which shows the ability of highly correlated (RHO =0.95) and TF-weighted noise speech with solvability. The performance of this method is significantly better than the other three more complex objective measurement methods.

​	The first model of the algorithm is a test procedure based on normalized covariance, which determines the correlation coefficient between the frequency band intensity envelope of the processed speech and the clean speech. The second model is the Complex Perception model (DAU), which can be used as a human observer to accurately predict the masking threshold of various masks. Its final distance measure is calculated by a linear correlation coefficient between the internal spectral time representations. The last model is a simple objective measure based on the normalized subband envelope correlation. This model shows very good results compared to the same IBM conditions. Firstly, tf decomposition is performed, then frequency normalization and compression are performed on the time envelope, and then DC is removed. The final result is averaged to calculate the correlation between all TF points of clean and processed speech.

​	Out of all the 168 ITFS-processing conditions, 75 conditions have a subjective intelligibility score above 80%. In order to prevent clustering for these high scores, which may bias the objective intelligibility prediction results, 41 randomly picked conditions, with a

score above 80%, are discarded. As a consequence, the scores of the remaining subset are approximately uniformly distributed between 0%-100%.

​	For each subset-condition, 30 fifive-word sentences are randomly chosen from the corpus and concatenated. The clean and processed signal are then segmented into 50% overlapping, Hanning

windowed frames with a length of 256 samples where the maximum energy frame of the clean speech is determined. Finally, both signals are reconstructed, excluding all the frames where the clean

speech energy is lower than 40 dB with respect to the maximum clean speech energy frame. With this procedure, time-frames with no signifificant speech energy (mainly silence regions), and therefore no contribution to the intelligibility, will not be included.To compare the results between the objective measures and the subjective intelligibility scores directly, a mapping is needed in order to account for a nonlinear relation between the objective and subjective values. For the proposed method, and the CSTI a logistic function is applied：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.15.30-20220619234318035.png" alt="截屏2022-06-18 12.15.30" style="zoom:50%;" />

while for DAU and NSEC a better fifit was observed with the following function：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.16.29-20220619234318103.png" alt="截屏2022-06-18 12.16.29" style="zoom:50%;" />

​	where *a*, *b* and *c* in (7) and (8) are free parameters, which are fifitted to the subjective data with a nonlinear least squares procedure, and *d* denotes the objective outcome. Due to better results with the latter proposed mapping for NSEC.The performance of all the objective measures is evaluated by means of the root of the mean squared prediction error (RMSE),

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.17.17-20220619234318231.png" alt="截屏2022-06-18 12.17.17" style="zoom:50%;" />

​	where *s* refers to the subjective score, *S* denotes the total number of conditions in the subset, and *i* runs over all subset-conditions.In addition, the correlation coeffificient between the subjective and objective data is calculated.

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.17.55-20220619234318292.png" alt="截屏2022-06-18 12.17.55" style="zoom:50%;" />



## 4 System Interface

A screenshot of our interface is as follows:

The system home page

![截屏2022-06-17 17.44.23](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.44.23-20220619234318602.png)

Algorithm introduction

![截屏2022-06-17 17.46.52](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.46.52-20220619234318896.png)

Localization

![](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.47.20-20220619233041660-20220619234319285.png)

Audio Recording interface

![截屏2022-06-17 17.48.56](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.48.56-20220619234319589.png)

Result Visulization

![截屏2022-06-17 17.49.55](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.49.55-20220619234320036.png)

Upload wav files

![截屏2022-06-17 17.50.24](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.50.24-20220619234320357.png)

Audio denies

![截屏2022-06-17 17.50.53](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.50.53-20220619234320635.png)

- ## 3 structures and modules of Back-end

- ### 3.1 The backend architecture

​	Our project back end use `flask`  for realizing the back-end service, at the same time use `tensorflow2.3.0`, `tqdm`, `resampy`, `pystoi`, `museval` library retrieval back-end algorithm, etc.

​	Flask uses restful apis to call background algorithms for audio quality evaluation and audio noise reduction.

​	We mainly implemented the following two apis：

| URL                    | Method | Params                        | Description                                                  | Return example                                               |
| ---------------------- | ------ | ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| BASEURL/audioQuality   | POST   | Algorithms: array audio: blob | The input audio file and algorithm return the index score and algorithm running time of the corresponding algorithm evaluation | {                              "mosnet": {                  "avgScore": 2.9970579147338867,        "score": [            3.083199977874756,            2.9672365188598633,            3.211167335510254,            2.726627826690674        ],        "time": 2750    }                    } |
| BASEURL/audioDenoising | POST   | Audio:blob                    | Pass in the audio blob file to be de-noised and return the de-noised audio file | {'audio':blob}                                               |

### 3.2 back-end project structure

The back-end Flask project file structure is as follows：

.

├── LICENSE

├── MANIFEST.in

├── README.md

├── Server

│  ├── rest-server.py

│  └── templates

│    └── main.html

├── algorithm

│  ├── data

│  │  └── readme.txt

│  └── speechAssessment.py

├── ffmpeg.exe

├── requirements.txt

├── setup.py

└── speechmetrics

  ├── __init__.py

  ├── __pycache__

  │  └── __init__.cpython-37.pyc

  ├── absolute

  │  ├── __init__.py

  │  ├── __pycache__

  │  │  └── __init__.cpython-37.pyc

  │  ├── mosnet

  │  │  ├── __init__.py

  │  │  ├── __pycache__

  │  │  │  ├── __init__.cpython-37.pyc

  │  │  │  └── model.cpython-37.pyc

  │  │  ├── cnn_blstm.h5

  │  │  └── model.py

  │  └── srmr

  │    ├── LICENSE.md

  │    ├── __init__.py

  │    ├── __pycache__

  │    │  ├── __init__.cpython-37.pyc

  │    │  ├── hilbert.cpython-37.pyc

  │    │  ├── modulation_filters.cpython-37.pyc

  │    │  ├── segmentaxis.cpython-37.pyc

  │    │  ├── srmr.cpython-37.pyc

  │    │  └── vad.cpython-37.pyc

  │    ├── hilbert.py

  │    ├── modulation_filters.py

  │    ├── segmentaxis.py

  │    ├── srmr.py

  │    └── vad.py

  └── relative

​    ├── __init__.py

​    ├── __pycache__

​    │  ├── __init__.cpython-37.pyc

​    │  ├── bsseval.cpython-37.pyc

​    │  ├── pesq.cpython-37.pyc

​    │  ├── sisdr.cpython-37.pyc

​    │  └── stoi.cpython-37.pyc

​    ├── bsseval.py

​    ├── pesq.py

​    ├── sisdr.py

​    └── stoi.py

The following describes the functions of important files：

| File name           | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Rest-server.py      | Flask main entry, containing API implementation              |
| speechAssessment.py | Algorithm main file, algorithm API implementation, call each algorithm |
| algorithm           | Algorithm folder, the connotation of six folders of the recurrence code |
| cnn_blstm.h5        | Deep learning algorithm MOSNET model training file           |



### 3.3 Part of introduction of Algorithms

#### 3.3.1 PESQ

PESQ is a proxy for non-deep learning audio quality evaluation.

Audio quality evaluation algorithms can be roughly divided into the following two categories.

1. Intrusive algorithm
2. Non - intrusive algorithm

​	PESQ is an **intrusive** audio quality evaluation algorithm. Intrusive means that the algorithm needs to use the noiseless standard audio of the audio as a reference, and obtain the quality of the input audio by comparing the frequency spectrum. This is where the limits of invasive algorithms lie.

​	The result index of PESQ algorithm is the well-known MOS index. The MOS metric uses a score of 0-5 to indicate audio quality. The higher the score, the better the audio quality.

​	The following are the criteria for MOS indicators：

| Audio Level | Evaluation Standand                                  | Corresponding MOS |
| ----------- | ---------------------------------------------------- | ----------------- |
| A           | clear and sound; low delay, fluent communication     | 4.0-5.0           |
| B           | clear; low delay but with mild blocking and noise    | 3.5-4.0           |
| C           | Slightly unclear；Have delay but okay to communicate | 3.0-3.5           |
| D           | Unclear；Severe delay and requires repetition        | 1.5-3.0           |
| E           | Unrecognizable；Severe delay with blocking           | 0-1.5             |

​	PESQ, as described in the standard, can carry out end-to-end audio quality testing, the reference signal (Reference speech) line in passed into the transmitter (the following figure is a telephone), after the telephone network to the receiving end, and then Line out passed out and directly back to the loop (Figure called the reference path Reference path) of the reference signal passed into the PESQ The algorithm proceeds, with reference evaluation, and finally generates the PESQ score.

A simple PESQ algorithm is as follow：

![v2-a133189ac2149596495439e1a4a2bc8c_1440w](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/v2-a133189ac2149596495439e1a4a2bc8c_1440w-20220619233538125-20220619234320810.jpg)

​	In brief, the time Alignment detects the input active speech segment, then performs the delay calculation and speech segmentation, and this algorithm is compatible with variable delays. Then the PESQ Algorithm calculates the aligned reference signal and the signal to be measured, gets their signals in the frequency domain with some compensation, and then transfers them to the loudness domain to compare the perceptual differences between the two signals according to the psychoacoustic model. Finally, the difference is mapped to a PESQ score similar to the MOS score, which ranges from -0.5 to 4.5.



#### 3.3.2 Mosnet

https://doi.org/10.48550/arXiv.1904.08352

​	Unlike PESQ, MOSnet uses deep learning algorithms to achieve non-Intrusive audio quality evaluation that is closer to human subjective ratings. In this algorithm, CNN-BLSTM is used as a deep learning network. Because the BLSTM has the characteristics of anterior-posterior correlation, it can integrate the before and after frame information of audio, making the frame evaluation of audio quality more accurate. It also integrates the advantages of convolutional neural network.

![截屏2022-06-17 17.00.38](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.00.38-20220619233539611-20220619234321490.png)

​	The model uses the data set shown above, which contains people's ratings of the audio conversion results, a natural audio quality corpus.

​	This paper proposes an objective evaluation method based on deep learning, which uses MOS to model human perception, called MOSNet. With the original amplitude spectrum as the input features and three new values, l network-based models, namely CNN, BLSTM and CNN-BLSTM, were used to extract valuable features from the input features of the fully connected (FC) layer to generate the predicted MOS. In the following sections, we'll look at each MOSNet component in detail. Using the extracted features, we use two FC layers to regression the frame-level features into a frame-level scalar to represent the naturalness score of each frame. Finally, a global averaging operation is where the application cheats the frame-level score to obtain the speech-level natural score.

![截屏2022-06-17 17.16.30](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.16.30-20220619233540499-20220619234321771.png)

​	This algorithm uses a loss function based on mean square error, so the results are mostly clustered between 2.5-3.5 points, presenting a Gaussian distribution.

#### 3.3.3 SRMR

The speech-to-reverberation modulation energy ratio (SRMR) is a non-intrusive metric for speech quality and intelligibility based on a modulation spectral representation of the speech signal. The metric was proposed by Falk et al. and recently updated for variability reduction and improved intelligibility estimation both for normal hearing listeners and cochlear implant users

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/Snipaste_2022-06-15_21-17-34-20220619233540743-20220619234322252.png" alt="Snipaste_2022-06-15_21-17-34" style="zoom:67%;" />

In order to reduce this difference,The SRMR thresholding will be calculated. The objective is to truncate extremely low energies, which lead to high ratios due to the division done in SRMR, and also limit the modulation energy dynamic range. In our modulation energy limitation scheme, we first compute the energy values for each of the acoustic and modulation frequencies in all frames, and then compute the average peak value.
$$
\bar{E}_{p e a k}=\max _{j, f_{b}}\left(\frac{1}{M} \sum_{m=1}^{M} E_{j}\left(m, f_{b}\right)\right)
$$

The average peak will be use as an upper threshold of the modulation energy in each band for all frames. Finally an lower bound will be manually set to truncate the extremely low energies.

#### 3.3.4 Bsseval

BSS Eval is a Matlab toolbox to measure the performance of (blind) source separation algorithms within an evaluation framework where the original source signals are available as ground truth [1,3. The measures are based on the decomposition of each estimated source signal into a number of contributions corresponding to the target source, interference from unwanted sources, and artifacts such as "musical noise". They are valid for any type of data (audio, biomedical, etc), any mixture (instantaneous, convolutive, etc) and any algorithm (beamforming, ICA, time-frequency masking, etc). By separating the audio we get: 



$$
\widehat{s}_{j}=s_{\text {target }}+e_{\text {interf }}+e_{\text {noise }}+e_{\text {artif }}
$$
The seperation result contains target, interference, noise and artifacts. For a good seperation audio, the first 3 metric values should be 0. The alogritm of the individual algorithm is:



$$
\
\begin{aligned}
s_{\text {target }} &:=P_{s_{j}} \widehat{s}_{j} \\
e_{\text {interf }} &:=P_{\mathbf{s}} \widehat{s}_{j}-P_{s_{j}} \widehat{s}_{j} \\
e_{\text {noise }} &:=P_{\mathbf{s}, \mathbf{n}} \widehat{s}_{j}-P_{\mathbf{s}} \widehat{s}_{j} \\
e_{\text {artif }} &:=\widehat{s}_{j}-P_{\mathbf{s}, \mathbf{n}} \widehat{s}_{j}
\end{aligned}
$$



which can be simply represented with vector diagram:

#### 3.3.5 SISDR 

​	SISDR is a scale-invariant SDR(SISDR) algorithm based on SDR(signal distortion ratio). The algorithm uses the following formula to calculate SNR. The relationship between SNR and SI-SDR is shown below.

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.00.02-20220619233540805-20220619234322422.png" alt="截屏2022-06-18 12.00.02" style="zoom:50%;" />

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2011.59.06-20220619233541210-20220619234322510.png" alt="截屏2022-06-18 11.59.06" style="zoom:50%;" />

​	To ensure that the residual is indeed orthogonal to the target, we can either rescale the target or rescale the estimate. Rescaling the target such that the residual is orthogonal to it corresponds to fifinding the orthogonal projection of the estimate *s*ˆ on the line spanned by the

target *s*, or equivalently fifinding the closest point to *s*ˆ along that line.This leads to two equivalent defifinitions for what we call the scale invariant signal-to-distortion ratio (SDR):

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.02.04-20220619233541484-20220619234322594.png" alt="截屏2022-06-18 12.02.04" style="zoom:50%;" />

下图直观显示了SISDR和SDR的对比：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.04.19-20220619233542022-20220619234322771.png" alt="截屏2022-06-18 12.04.19" style="zoom:50%;" />

#### 3.3.6 STOI

Paper addresses： https://ieeexplore.ieee.org/abstract/document/5495701

​	The algorithm presents an objective solvability measure, which shows the ability of highly correlated (RHO =0.95) and TF-weighted noise speech with solvability. The performance of this method is significantly better than the other three more complex objective measurement methods.

​	The first model of the algorithm is a test procedure based on normalized covariance, which determines the correlation coefficient between the frequency band intensity envelope of the processed speech and the clean speech. The second model is the Complex Perception model (DAU), which can be used as a human observer to accurately predict the masking threshold of various masks. Its final distance measure is calculated by a linear correlation coefficient between the internal spectral time representations. The last model is a simple objective measure based on the normalized subband envelope correlation. This model shows very good results compared to the same IBM conditions. Firstly, tf decomposition is performed, then frequency normalization and compression are performed on the time envelope, and then DC is removed. The final result is averaged to calculate the correlation between all TF points of clean and processed speech.

​	Out of all the 168 ITFS-processing conditions, 75 conditions have a subjective intelligibility score above 80%. In order to prevent clustering for these high scores, which may bias the objective intelligibility prediction results, 41 randomly picked conditions, with a

score above 80%, are discarded. As a consequence, the scores of the remaining subset are approximately uniformly distributed between 0%-100%.

​	For each subset-condition, 30 fifive-word sentences are randomly chosen from the corpus and concatenated. The clean and processed signal are then segmented into 50% overlapping, Hanning

windowed frames with a length of 256 samples where the maximum energy frame of the clean speech is determined. Finally, both signals are reconstructed, excluding all the frames where the clean

speech energy is lower than 40 dB with respect to the maximum clean speech energy frame. With this procedure, time-frames with no signifificant speech energy (mainly silence regions), and therefore no contribution to the intelligibility, will not be included.To compare the results between the objective measures and the subjective intelligibility scores directly, a mapping is needed in order to account for a nonlinear relation between the objective and subjective values. For the proposed method, and the CSTI a logistic function is applied：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.15.30-20220619233542184-20220619234322902.png" alt="截屏2022-06-18 12.15.30" style="zoom:50%;" />

while for DAU and NSEC a better fifit was observed with the following function：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.16.29-20220619233542264-20220619234323344.png" alt="截屏2022-06-18 12.16.29" style="zoom:50%;" />

​	where *a*, *b* and *c* in (7) and (8) are free parameters, which are fifitted to the subjective data with a nonlinear least squares procedure, and *d* denotes the objective outcome. Due to better results with the latter proposed mapping for NSEC.The performance of all the objective measures is evaluated by means of the root of the mean squared prediction error (RMSE),

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.17.17-20220619233542337-20220619234323761.png" alt="截屏2022-06-18 12.17.17" style="zoom:50%;" />

​	where *s* refers to the subjective score, *S* denotes the total number of conditions in the subset, and *i* runs over all subset-conditions.In addition, the correlation coeffificient between the subjective and objective data is calculated.

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-18%2012.17.55-20220619233542489-20220619234324132.png" alt="截屏2022-06-18 12.17.55" style="zoom:50%;" />



## 4 System Interface

A screenshot of our interface is as follows:

The system home page

![截屏2022-06-17 17.44.23](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.44.23-20220619233544917-20220619234325351.png)

Algorithm introduction

![截屏2022-06-17 17.46.52](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.46.52-20220619233546298-20220619234325994.png)

Localization

![](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.47.20-20220619233547681-20220619234327014.png)

Audio Recording interface

![截屏2022-06-17 17.48.56](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.48.56-20220619233548473-20220619234327842.png)

Result Visulization

![截屏2022-06-17 17.49.55](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.49.55-20220619233548773-20220619234328380.png)

Upload wav files

![截屏2022-06-17 17.50.24](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.50.24-20220619233549570-20220619234328918.png)

Audio denies

![截屏2022-06-17 17.50.53](https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%88%AA%E5%B1%8F2022-06-17%2017.50.53-20220619233549837-20220619234329183.png)

## 5 Advantage & Disadvantages

### 5.1 Advantages

#### 5.1.1  Clear Introduction

This project provided a usage demonstration for 6 different sound quality metric algorithm, which may be hard to tell the difference for ordinary users. For that, we provide introduction with markdown and formula on the front page of our repo, and a video showing our system’s operation flow is provided as well. By clicking the card and the video widget, user can get clear background info for the algorithm and sound quality metric.

#### 5.1.2 Localization

Our program uses i18n as a localization for the below language support:

- Chinese
- English

By clicking the button on the top right zone of the app bar, user can translate the webpage content between Chinese and English in a real quick speed. Every character string in our system will be translated, leaving no language gap for our system.

#### 5.1.3 Input Usability

We allow users to input the audio by:

- upload an existed audio file (.wav)
- record instantly by clicking the “record“ button

By allowing instant record, the user can use our system online or offline. 

#### 5.1.4 Visualization

The system’s main functionality is to demonstrate sound quality score and de-noise the record file(.wav), For a clear view of representing the score, we completes the following tasks on the aspects of visualization:

**Data and view specification** 

- Visualize: we use wavesurfer.js to visualize the record file’s sound wave graph, which describes the feature of the sound, as well as the result of audio de-noising.
- Filter: user can choose different algorithm to get sound quality score, and the output depends on the type of the evaluation algorithm with different sound metrics.
- Derive: additional data like algorithm preprocessing time, overall score is calculated and compared in graph
- Graph: Different types of graph is implemented to show the data, with standard graph types from sound metrics usual charts.

**Process and provenance**

- Download: our system provides result download for audio de-noising.
- Guide: the result analysis and some tips for metrics will be shown when the mouse is hovered on graph widgets.
- Compare: The result of the original audio file and the de-noised file will be compared in wave graph, showing the de-noising effect for our system.

### 5.2 Disadvantages

#### 5.2.1 Complex Contents

Our work relates to certain scientific topics for sound process and some complex algorithms that requires expert domain knowledge. It may be difficult for normal user to understand our system’s usage and the metrics we apply in our system.

#### 5.2.2 Lack Supports for some main streaming algorithms

We only implemented 6 sound quality evaluation algorithm for our system, leaving out some other algorithms that is also very main streaming and important (PESQA, for example).This may disappoint some of our target users’ rate because some of their desired models are not supported.

## 6 How to improve our system

### 6.1 Improve user usability by lower the learning difficulty

We can bring more examples for how to use our system in our user guidance or contents in our website (for instance, explaining the usage for sound quality and audio de-noising, giving samples for input in different zone in our system rather than explaining them just through one video in our homepage).

### 6.2 Support more algorithm in the future

Due to time limits, we left out some important algorithms for sound quality that will makes our system more complete. As an improvement, we surely need to add them to the system to meet more target users’ expectation.
