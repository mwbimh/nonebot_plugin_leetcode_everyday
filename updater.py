import asyncio
from playwright.async_api import async_playwright
from typing import Dict
from aiohttp import ClientSession
import json
import nonebot

session = ClientSession()


# async def update_today():
#     try:
#         get_today_data = await session.post("https://leetcode-cn.com/graphql", json={
#             "query": "query questionOfToday {todayRecord { date question {frontendQuestionId: questionFrontendId difficulty titleSlug } } } ",
#             "variables": {}
#             })
#         today_data = json.loads(await get_today_data.text())
#         title = today_data["data"]["todayRecord"][0]["question"]["titleSlug"]
#         url = "https://leetcode-cn.com/problems/" + title
#         response = await session.post(
#             "https://leetcode-cn.com/graphql",
#             json={"operationName": "questionData", "variables": {"titleSlug": title},
#             "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
#         # 转化成json格式
#         # print(1)
#         # jsonText = await response.text()
#         # print(jsonText)
#         jsonText = json.loads(await response.text()).get('data').get("question")
#         # 题目题号
#         no = jsonText.get('questionFrontendId')
#         # 题名（中文）
#         leetcodeTitle = jsonText.get('translatedTitle')
#         # 题目难度级别
#         level = jsonText.get('difficulty')
#         # 题目内容
#         context = jsonText.get('translatedContent')
#         q = f"{no}.{leetcodeTitle}\n{level}\n{context}\n来源:{url}"

#         # nonebot.log.logger.debug("html:{}".format(json.dumps(jsonText)))
#         return q
#     except Exception as e:
#         raise e



# 以下为使用无头浏览器的截图更新，内存消耗较大所以没有测试
page = None
p = None
b = None
Size = Dict[str, int]


async def prepare_page(size: Size):
    global page
    global p
    global b
    p = await async_playwright().start()
    b = await p.firefox.launch()
    page = await b.new_page(viewport=size)


async def update_today():
    try:
        get_today_data = await session.post("https://leetcode-cn.com/graphql", json={
            "query": "query questionOfToday {todayRecord { date question {frontendQuestionId: questionFrontendId difficulty titleSlug } } } ",
            "variables": {}
            })
        today_data = json.loads(await get_today_data.text())
        title = today_data["data"]["todayRecord"][0]["question"]["titleSlug"]
        url = "https://leetcode-cn.com/problems/" + title
        response = await session.post(
            "https://leetcode-cn.com/graphql",
            json={"operationName": "questionData", "variables": {"titleSlug": title},
            "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
        jsonText = await response.text()
        jsonText = json.loads(await response.text()).get('data').get("question")
        # 题目题号
        no = jsonText.get('questionFrontendId')
        # 题名（中文）
        leetcodeTitle = jsonText.get('translatedTitle')
        # 题目难度级别
        level = jsonText.get('difficulty')
        # 题目内容
        q = jsonText.get('translatedContent')
        content = f"<html>\
                        <body>\
                            <h1>{no}.{leetcodeTitle}</h1>\
                            <h2>{level}</h2>\
                            <div>{q}</div>\
                        </body>\
                    </html>"
        await page.set_content(content, wait_until="load")
        # div = page.locator("[data-key=description-content]")
        return await page.screenshot(full_page=True), f"来源:{url}"
    except Exception as e:
        raise e


async def shutdown_page():
    await b.close()
    await p.stop()
    await session.close()


async def set_page_size(size: Size):
    global page
    page.set_viewport_size(size)


# async def html_to_pic(
#     html: str, wait: int = 0, template_path: str = f"file://{getcwd()}", **kwargs
# ) -> bytes:
#     """html转图片
#     Args:
#         html (str): html文本
#         wait (int, optional): 等待时间. Defaults to 0.
#         template_path (str, optional): 模板路径 如 "file:///path/to/template/"
#     Returns:
#         bytes: 图片, 可直接发送
#     """
#     # logger.debug(f"html:\n{html}")
#     if "file:" not in template_path:
#         raise "template_path 应该为 file:///path/to/template"
#     async with get_new_page(**kwargs) as page:
#         await page.goto(template_path)
#         await page.set_content(html, wait_until="networkidle")
#         await page.wait_for_timeout(wait)
#         img_raw = await page.screenshot(full_page=True)
#     return img_raw
