# -*- encoding: UTF-8 -*-

''' Example showing how to use python to make the Robot move and talk
    by using a proxy to ALMotion and ALTextToSpeech'''

import argparse
import time

from naoqi import ALProxy

def main(robotIP, PORT=9559):

    # Create a proxy to ALMotion.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e

    # Create a proxy to ALRobotPosture.
    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ",e

    # Create a proxy to ALTextToSpeech
    try:
        speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ",e

    # WakeUp
    motionProxy.wakeUp()

    # Stand up.
    postureProxy.goToPosture("StandInit", 0.3)

    chainName = "RArm"
    frame = 1 # FRAME_WORLD
    useSensors = True

    speechProxy.languages = speechProxy.getAvailableLanguages()
    if 'French' in speechProxy.languages:
        speechProxy.setLanguage('French')
        speechProxy.setLanguageDefaultVoice('French', 'aurelie')
    else:
        speechProxy.setLanguage('English')

    speechProxy.voices = speechProxy.getAvailableVoices()
    speechProxy.sent_config_pour = "Je suis configuré pour parler en "
    speechProxy.sent_greetings = "Hello la team de Bordeaux"
    speechProxy.sent_6po = "Comme mon ancêtre 6 p o ,  je maitrise six millions de formes de communication parmi lesquelles figurent les langues suivantes"
    speechProxy.sent_plusieurs_voix_open = "Je peux changer de voix"
    speechProxy.sent_plusieurs_voix_close = "Pas mal hein ?"
    speechProxy.sent_closing = "J'espère que vous avez apprécié. C'était un premier test pour m'échauffer la voix. A bientôt"

    speechProxy.say(speechProxy.sent_config_pour)
    speechProxy.say(speechProxy.locale())
    # speechProxy.onStopped() #activate the output of the box
    speechProxy.say(speechProxy.sent_greetings)

    postureProxy.goToPosture("Stand", 0.6)

    speechProxy.say(speechProxy.sent_6po)
    speechProxy.setLanguage('English')
    for lang in speechProxy.languages:
        speechProxy.say(lang)
        time.sleep(0.25)

    speechProxy.say(speechProxy.sent_plusieurs_voix_open)

    for voice in speechProxy.voices:
        speechProxy.setVoice(voice)
        speechProxy.say(voice)
        time.sleep(0.25)

    speechProxy.setLanguage('French')
    speechProxy.say(speechProxy.sent_plusieurs_voix_close)
    speechProxy.say(speechProxy.sent_closing)


    # Time to go to bed
    time.sleep(2.0)
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=53058,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)