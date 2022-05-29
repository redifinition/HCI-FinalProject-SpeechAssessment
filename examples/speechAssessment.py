import speechmetrics as sm
import pprint
from audoai.noise_removal import NoiseRemovalClient
noise_removal = NoiseRemovalClient(api_key='c70f68814902e8705aa9d16ac84e91bf')
window = 15

# 使用单个方法进行语音质量评价
# 可供选择的方法：
# absolute_relative = "absolute",method = 'mosnet'
# absolute_relative = "absolute",method = 'srmr'
# absolute_relative = "relative",method = 'bsseval'
# absolute_relative = "relative",method = 'pesq'
# absolute_relative = "relative",method = 'sisdr'
# absolute_relative = "relative",method = 'stoi'
def single_speech_assessment(wav_url, absolute_relative="relative", method="pesq"):
    metrics = sm.load(absolute_relative + '.' + method,window)
    tests = wav_url

    # 侵入式
    if absolute_relative == 'relative':
        # 根据语音增强接口生成降噪音频即参照的音频
        # 由于本api收费，在debug时请注释掉下面两行代码
        #reference_result = noise_removal.process(wav_url)
        #reference_result.save('data/clean_audio.wav')
        reference = 'data/clean_audio.wav'
        scores = metrics(reference,tests)

    # 非侵入式
    else:
        scores = metrics(tests)
    pprint.pprint(scores)
    return scores


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
    # reference_result = noise_removal.process(wav_url)
    # reference_result.save('data/clean_audio.wav')
    reference = 'data/clean_audio.wav'
    scores = metric_relative(reference, test)
    result.update(scores)
    return result

single_speech_assessment('data/m2_script1_ipad_confroom1.wav', 'absolute', 'mosnet')
single_speech_assessment('data/m2_script1_clean.wav', 'absolute', 'mosnet')
single_speech_assessment('data/m2_script1_produced.wav', 'absolute', 'mosnet')

speech_assessment_all('data/m2_script1_ipad_confroom1.wav')
