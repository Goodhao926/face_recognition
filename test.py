def char(data):
    wx = wx_deal()
    # 表情处理
    if (data.find('表情') != -1):
        if (data.find('文本') != -1):
            data = data.replace('表情', '')
            data = data.replace('文本', '')
            result = GetExpression_Search(data)
            msg_type = 'text'

            text = ''
            for i in range(5):
                text += result[i][1] + ':' + result[i][0] + '\n'
            return text, msg_type
        else:
            data = data.replace('表情', '')
            result = GetExpression_Search(data)
            msg_type = 'image'
            local = 'c:/wxpublic/temp.gif'

            if len(result) != 0:
                dowload_photo(result[0][0], local)
                img_id = wx.updata_photo(local)
                return img_id, msg_type

