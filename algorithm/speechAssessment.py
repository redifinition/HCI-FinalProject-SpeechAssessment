import speechmetrics as sm
import pprint
from audoai.noise_removal import NoiseRemovalClient
noise_removal = NoiseRemovalClient(api_key='c70f68814902e8705aa9d16ac84e91bf')
window = 2

ALGORITHM_INFO = {"mosnet":"absolute",
                  "srmr":"absolute",
                  "bsseval":"relative",
                  "pesq":"relative",
                  "sisdr":"relative",
                  "stoi":"relative"}
# 使用单个方法进行语音质量评价
# 可供选择的方法：
# absolute_relative = "absolute",method = 'mosnet'
# absolute_relative = "absolute",method = 'srmr'
# absolute_relative = "relative",method = 'bsseval'
# absolute_relative = "relative",method = 'pesq'
# absolute_relative = "relative",method = 'sisdr'
# absolute_relative = "relative",method = 'stoi'
def single_speech_assessment(wav_url, method="pesq",use = True):
    import time
    absolute_relative = ALGORITHM_INFO.get(method)
    metrics = sm.load(absolute_relative + '.' + method,window)
    tests = wav_url
    # 侵入式
    if absolute_relative == 'relative':
        # 根据语音增强接口生成降噪音频即参照的音频
        # 由于本api收费，在debug时请注释掉下面两行代码
        if use:
            reference_result = noise_removal.process(wav_url)
            reference_result.save('../algorithm/data/clean_audio.wav')
        reference = '../algorithm/data/clean_audio.wav'
        time_before = time.process_time()
        scores = metrics(reference,tests)
        time_after = time.process_time()

    # 非侵入式
    else:
        time_before = time.process_time()
        scores = metrics(tests)
        time_after = time.process_time()
    result = {}
    result["score"] = scores
    result["time"] = round(time_after - time_before,6)*1000
    if method == 'mosnet':
        result["time"] = result["time"]/2
    print(result)
    return result

#输入降噪前的音频，输出降噪后的音频
def denoise(wav_url):
    return noise_removal.process(wav_url)

# 输入wav文件，输出使用全部六种方法的评价分数
# 注意结果中的isr,sdr,sar是sisdr中的结果，三者是一起的
def speech_assessment_all(wav_url):
    result = {}
    test = wav_url
    # 绝对的方法
    metric_absolute = sm.load('absolute',window)
    scores = metric_absolute(wav_url)
    result = scores

    # 相对的方法
    metric_relative = sm.load('relative',window)
    # 根据语音增强接口生成降噪音频即参照的音频
    # 由于本api收费，在debug时请注释掉下面两行代码
    reference_result = noise_removal.process(wav_url)
    print(reference_result.url)
    reference_result.save('../algorithm/clean_audio.wav')
    reference = '../algorithm/clean_audio.wav'
    scores = metric_relative(reference, test)
    result.update(scores)
    return result

# single_speech_assessment('test.wav',  'mosnet')
# single_speech_assessment('data/m2_script1_clean.wav', 'mosnet')
# single_speech_assessment('../algorithm/test.wav', 'bsseval')
#
# speech_assessment_all('data/m2_script1_ipad_confroom1.wav')
