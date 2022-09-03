import json
import sys

warningInformation = "[[Question:Text]]\n<strong>Warning:</strong> This survey may present situations that are triggering due to their socially unacceptable nature including a variety of not-safe-for-work (NSFW) or other examples. "\
    "If at any time you feel uncomfortable while completing the survey, please exit. Any incomplete responses will be destroyed.\n\n<br><br><strong>Data Collection:</strong> Your IP, nation of origin, browser type and other information may "\
    "be collected. Screening questions and filters used to distribute this survey on <em><strong>Prolific</strong></em> allow researchers to filter survey availability for certain demographics. <u>Though not specifically collected or attached to responses</u>"\
    ", the researchers conducting this study may be able to infer your capability to speak English or education level. <u>Your country of origin may be attached to this data in further modifications or transformations thereof</u>. "\
    "\n\n<br><br><strong>Progress:</strong> You may at any time return to a previous page but <u style=\"color:#9b59b6\">please do not use your browser's back button</u>. Find the back arrow button either at "\
    "the top or bottom of the survey page itself.\n\n"

initialInstructions = "[[Question:Text]]\n<strong style=\"font-size:24px;\">INSTRUCTIONS:</strong>\n\n<br><br>You will be presented with a short story that will fall into a certain categorization. Do not worry about grammatical or spelling errors. For example:"\
    "\n\n<br><br><i>He smiled briefly at her . then he reiterated something he said earlier. he laid out several scenarios. they ranged from minor inconveniences to very serious ones. in the end, he told her to relax.</i>\n\n<br><br>For each story, you will be tasked "\
    "to select a categorization from a given list. As an example, for the previous story, you may be presented with the following:\n\n<br><br><ul><li>Good</li><li>Neutral</li><li>Bad</li></ul>\n\n<br><br>In this case, you are asked to determine the <i>ethical/moral alignment</i> "\
    "of the story. A reasonable answer for this example may be <strong>Neutral</strong>. The question will specify what the options mean in relation to the story.\n\n"

extraExample = "[[Question:Text]]\nAs another example: \n\n<br><br><i>alex's favorite rock band performs tonight. they played the song one time every week they are famous for. alex loves to listen to them.</i>\n\n<br><br>In this case, you may be presented with the following choices:\n\n<br><br>"\
    "<ul><li><i>Family</i></li><li><i>Music</i></li><li><i>Accident/Disaster</i></li><li><i>Religion</i></li><li><i>Imagery</i></li><li><i>Fighting</i></li>\n\n<br><br></ul>You will be tasked with choosing the <i>topic</i> that relates the most to the short story. A reasonable answer for this example may be <strong>Music</strong>.\n\n"

finalExample = "[[Question:Text]]\nAs a final example, you may be presented with the following story:\n\n<br><br><i>His mind rolled back again and he cried silently to himself. he awoke from the nightmare. the monster stood before him. they stared at each other for a long time. he realized he was never going to get over that night.</i>\n\n<br><br>In this case, your options may be:\n\n<br><br>"\
    "<ul><li><em>Romance</em></li><li><em>Horror</em></li></ul>\n\n<br><br>For this example, a reasonable answer may be <strong>Horror</strong>\n\n"

freeResponseInstructions = "[[Question:Text]]\nYou may also be given the option to write in a categorization that is not provided as one of the options. However, this option should only be used if the short story cannot be categorized by <i>any of the given choices</i>. Otherwise, please select the best option from the provided categories.\n\n"

firstSectionInstructions = "[[Question:Text]]\nNow we will begin the first section. In this section, you will be provided a short story and you will be selecting the moral/ethical alignment of the story. The options will be good, neutral, and evil.\n\n<br><br>If the short story is <i>morally good</i>, select <strong>good</strong>.\n\n<br><br>"\
    "If the short story is <i>morally neutral</i>, select <strong>neutral</strong>.\n\n<br><br>If the short story is <i>morally evil</i>, select <strong>evil</strong>.\n\n"

secondSectionInstructions = "[[Question:Text]]\nNow we will begin the second section. In this section, you will be provided a short story and you will be selecting the <i>topic</i> of the story. Your options will be <i>family</i>, <i>music</i>, <i>accident/disaster</i>, <i>religion</i>, <i>imagery</i>, <i>fighting</i>, <i>romance</i>, and <i>horror</i>. If the story does not belong in <i>any</i> of the topics, you may provide your own.\n\n"\
    "You will select:\n\n<br><br><ul><li><i>Family</i> if the passage mainly discusses or features familial matters.</li><li><i>Music</i> if the passage mainly discusses or features musical matters</li><li><i>Accident/Disaster</i> if the passage discusses an accident/disaster or an accident/disaster occurs within the passage.</li><li><i>Religion</i> if the passage discusses non-secular (religious) matters.</li><li><i>Imagery</i> if the passage uses distinct discriptive language or is particularly detailed.</li><li><i>Fighting</i> if the passage discusses violence that could be characterized as fighting.</li><li><i>Romance</i> if the passage seems romantic or discusses topics relating to romance</li><li><i>Horror</i> if the passage is scary/horrific.</li></ul>\n\n"

#thirdSectionInstructions = "[[Question:Text]]\nNow we will begin the third section. In this section, you will be provided a short story and you will be selecting the <i>genre</i> of the story. Your options will be <i>romance</i> and <i>horror</i>.\n\n"

alignmentQuestion = [{'questionType':'singleSelect', 'answerOptions' : ['Good', 'Neutral', 'Evil'], 'questionPrompt':'Which <i>moral alignment</i> best describes this story?'}]

topicQuestion = [{'questionType':'singleSelect', 'answerOptions' : ['Family', 'Music', 'Accident/Disaster', 'Religion', 'Imagery', 'Fighting', 'Romance', 'Horror', 'Other:'], 'questionPrompt':'Which <i>topic</i> best describes this story?'}]

screeningQuestion = [{'passage':'Passage:<br><br>\n\n \'Are you afraid of the dark?\' That was the last thing I heard before the lightbulb shattered behind me.','questionType':'singleSelect', 'answerOptions' : ['Family', 'Music', 'Accident/Disaster', 'Religion', 'Imagery', 'Fighting', 'Romance', 'Horror', 'Other:'], 'questionPrompt':'Which <i>topic</i> best describes this story?'}]

#genreQuestion = [{'questionType':'singleSelect', 'answerOptions' : ['Romance', 'Horror'], 'questionPrompt':'Which <i>genre</i> best applies to this story?'}]

class StoryPair(dict):
    def __init__(self, jsonObjectStory):
        self.passage = jsonObjectStory['passage']
        self.model = jsonObjectStory['model']
        self.label = jsonObjectStory['label']

def addTextToQualtricsFile(fileName,text):
    with open(fileName, 'a') as f:
        f.write(text)

#def addExamplesToQualtricsFile():
#    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
#    addTextToQualtricsFile(sys.argv[2], firstSectionInstructions)
#    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')
#
#    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
#    addTextToQualtricsFile(sys.argv[2], secondSectionInstructions)
#    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

    #addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    #addTextToQualtricsFile(sys.argv[2], thirdSectionInstructions)
    #addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

#MAIN TODO HERE:
def createQuestionForQualtricsFile(fileName,ep):
    with open(fileName, 'a') as f:
        if ep.label.lower() == "good" or ep.label.lower() == "neutral" or ep.label.lower() == "evil":
            f.write('[[Question:MC:SingleAnswer]]\n')
            f.write('Passage:<br><br>\n\n' + ep.passage + '<br><br>' + alignmentQuestion[0]['questionPrompt'])
            f.write('\n')
            f.write('[[Choices]]')
            f.write('\n')
            for option in alignmentQuestion[0]['answerOptions']:
                f.write(option)
                f.write('\n')
            f.write("\n\n")
        #elif ep.label.lower() == "romance" or ep.label.lower() == "horror":
        #    f.write('[[Question:MC:SingleAnswer]]\n')
        #    f.write('Passage:<br><br>\n\n' + ep.passage + '<br><br>' + genreQuestion[0]['questionPrompt'])
        #    f.write('\n')
        #    f.write('[[Choices]]')
        #    f.write('\n')
        #    for option in genreQuestion[0]['answerOptions']:
        #        f.write(option)
        #        f.write('\n')
        #    f.write("\n\n")
        else:
            f.write('[[Question:MC:SingleAnswer]]\n')
            f.write('Passage:<br><br>\n\n' + ep.passage + '<br><br>' + topicQuestion[0]['questionPrompt'])
            f.write('\n')
            f.write('[[Choices]]')
            f.write('\n')
            for option in topicQuestion[0]['answerOptions']:
                f.write(option)
                f.write('\n')
            f.write("\n\n")


def addInstructionsToQualtricsFile():

    addTextToQualtricsFile(sys.argv[2],'[[AdvancedFormat]]\n\n')
    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    addTextToQualtricsFile(sys.argv[2], warningInformation)
    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    addTextToQualtricsFile(sys.argv[2], initialInstructions)
    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    addTextToQualtricsFile(sys.argv[2], extraExample)
    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    addTextToQualtricsFile(sys.argv[2], finalExample)
    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

    addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
    addTextToQualtricsFile(sys.argv[2], freeResponseInstructions)
    addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

def main():
    addInstructionsToQualtricsFile()
    #addExamplesToQualtricsFile()

    result = {}

    json_file_range = open(sys.argv[1])
    json_list_range = json_file_range.readlines()

    for idx,json_str in enumerate(json_list_range):
        result = json.loads(json_str)
        print(f"result: {result}")
        print(isinstance(result, dict))
            
        storyObj = StoryPair(result)
        if idx == 0 or idx == 92:
        #or idx == 131:
            if idx == 0:
                addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
                addTextToQualtricsFile(sys.argv[2], firstSectionInstructions)
                addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')
            elif idx == 92:
                addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
                addTextToQualtricsFile(sys.argv[2], secondSectionInstructions)
                addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')
                addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n')
                addTextToQualtricsFile(sys.argv[2], '[[Question:MC:SingleAnswer]]\n')
                addTextToQualtricsFile(sys.argv[2], screeningQuestion[0]['passage'] + '<br><br>' + screeningQuestion[0]['questionPrompt'])
                addTextToQualtricsFile(sys.argv[2], '\n')
                addTextToQualtricsFile(sys.argv[2], '[[Choices]]')
                addTextToQualtricsFile(sys.argv[2], '\n')
                for option in screeningQuestion[0]['answerOptions']:
                    addTextToQualtricsFile(sys.argv[2], option)
                    addTextToQualtricsFile(sys.argv[2], '\n')
                addTextToQualtricsFile(sys.argv[2], '\n\n')
                addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')

            addTextToQualtricsFile(sys.argv[2],'[[Block]]\n\n') #Each pair will be within a block
        createQuestionForQualtricsFile(sys.argv[2],storyObj)
        addTextToQualtricsFile(sys.argv[2],'[[PageBreak]]\n\n')
if __name__ == '__main__':
    main()

#Use: python get-qualtrics-story.py file.jsonl output.txt