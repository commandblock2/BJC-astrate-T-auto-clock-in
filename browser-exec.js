// https://stackoverflow.com/questions/9192956/getting-previous-date-using-javascript/9193127#9193127
Date.prototype.addDays = function (n) {
    var time = this.getTime();
    var changedDate = new Date(time + (n * 24 * 60 * 60 * 1000));
    this.setTime(changedDate.getTime());
    return this;
};

var date_ = new Date(date)
date_.addDays(-1)

var get_url = `https://yqfk.bjut.edu.cn/api/home/display/user_data_detail/${student_id}/${auth}/${date_.toISOString().split('T')[0]}`
var post_url = `https://yqfk.bjut.edu.cn/api/home/butian/daily_store?gh=${student_id}${auth_id_date}`

var xhr = new XMLHttpRequest()
xhr.open("GET", get_url, false)
bearer = uni.getStorageSync('token')
xhr.setRequestHeader("Content-Type", "application/json")
xhr.setRequestHeader("Authorization", "Bearer " + bearer)
xhr.send()

var data = JSON.parse(xhr.responseText)
    .data
    .question
    .filter(element => {
        return element.user_select_answer != null
    })
    .map(element => {
        return {
            "question_id": element.user_select_answer.question_id,
            "answer": {
                id: element.user_select_answer.answer_id,
                text: element.user_select_answer.answer_value_text
            }
        }
    })

var post_string = JSON.stringify(data)

var xhr = new XMLHttpRequest()
xhr.open("POST", post_url, false)
bearer = uni.getStorageSync('token')
xhr.setRequestHeader("Content-Type", "application/json")
xhr.setRequestHeader("Authorization", "Bearer " + bearer)
xhr.send(post_string)
return xhr.responseText