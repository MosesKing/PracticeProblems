import json


postContentString = {
    "paragraphs": [
    {
        "id": "p0",
        "text": "aaa"
    },
    {
        "id":"p1",
        "text":"bbb"
    },
    {
        "id": "p2",
        "text": "ccc"
    },
    {
        "id": "p3",
        "text": "ddd"
    },
    {
        "id": "p4",
        "text": "eee"
     },
    {
        "id": "p5",
        "text": "fff"
    }
],
    "sections": [
        {
            "id":"s0",
            "startIndex": 0
        },
        {
            "id": "s1",
            "startIndex": 2
        },
        {
            "id": "s2",
            "startIndex": 4
        }
    ]
}

def solution(postContentString):
    # variables
    postContent = json.loads(postContentString)
    paragraphs = postContent["paragraphs"]
    sections = postContent["sections"]
    startIndexes = []
    res = []
    # make sure the input is okay.
    try:
        # collect the indexes
        for section in sections:
            startIndexes.append(section['startIndex'])
        # iterate over and insert the groups, sections and new lines
        for i, paragraph in enumerate(paragraphs, start=1):
            if i == len(paragraphs):
                res.append(paragraph['text'])
            elif i in startIndexes:
                res.append(paragraph['text'] + '\n-\n')
            else:
                res.append(paragraph['text'] + '\n')

    except (KeyError, ValueError) as e:
        print("ERROR - input is not formated correctly")

    # return to main calling function
    return ''.join(res)


  
 ## ADDING MORE FUNCTIONALITY BECAUSE I NEEDED TO REFORMAT FOR THE NEXT QUESTION

def solution(postContentString, deltasString):
    postContent = json.loads(postContentString)
    deltas = json.loads(deltasString)

    # iterate through the deltas and collect the types and indexes present/expected from input
    for delta in deltas:
        try:
            deltaType = delta["type"]
            deltaIndex = delta["paragraphIndex"]
            # check to make sure the delta is valid
            if deltaIndex < 0 or deltaIndex >= len(postContent["paragraphs"]):
                continue
        except(KeyError, IndexError) as er:
            continue
        ## lets do the update paragraph part
        if deltaType == "updateParagraph":
            try:
                deltaParagraphText = delta["paragraph"]["text"]
                postContent["paragraphs"][deltaIndex]['text'] = deltaParagraphText

            except IndexError:
                continue
        ## let's do the add paragraph part
        elif deltaType == "addParagraph":
            try:
                addDelta = delta["paragraph"]
                postContent["paragraphs"].insert(deltaIndex, addDelta)
                # make sure the indexes are still are right
                i = deltaIndex
                while i < len(postContent["sections"][deltaIndex:]) + 1:
                    postContent["sections"][i]["startIndex"] += 1
                    i += 1
            except IndexError:
                continue
        ## let's do the delete part
        elif deltaType == "deleteParagraph":
            try:
                postContent["paragraphs"].pop(deltaIndex)
                i = deltaIndex
                while i < len(postContent["sections"][deltaIndex:]) + 1:
                    postContent["sections"][i]["startIndex"] -= 1
                    i += 1
                # fixes the indees are still right and like the solution says to make sure no blank sections -
                i = 1
                for i, section in enumerate(postContent["sections"]):
                    if section["startIndex"] <= 0:
                        postContent["sections"].pop(i)

            except IndexError:
                continue
    try:
        ## reiterate through and reformat the input to how defined in the last solutions.
        sections = postContent["sections"]
        paragraphs = postContent["paragraphs"]

        sectionIndex = set()
        for section in sections:
            sectionIndex.add(section["startIndex"])

        res = []

        for i, paragraph in enumerate(paragraphs, start=1):

            if i == len(paragraphs):
                res.append(paragraph["text"])
            elif i in sectionIndex:
                res.append(paragraph["text"] + '\n-\n')
            else:
                res.append(paragraph["text"] + '\n')

    except(KeyError, ValueError) as e:
        print("ERROR: ~ Input data is bad")

    return ''.join(res)
  
  
if __name__ == '__main__':
    solution(postContentString)
