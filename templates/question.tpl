<!-- 题目{{ q }} -->
<div class="question" id="q{{ q }}">
    <h3>{{ q }}、【多选题-少选或多选均不得分】{{ stem }}</h3>
    <img src="https://raw.githubusercontent.com/${{ github.repository }}/main/dist/image{{ q }}.png" alt="题目{{ q }}配图">
    <div class="options">
        {% for opt in opts %}
        <label><input type="checkbox" value="{{ opt[:1] }}"><span>{{ opt }}</span></label>
        {% endfor %}
    </div>
    <div class="feedback" id="f{{ q }}"></div>
    <button class="btn" onclick="check({{ q }})">提交答案</button>
    <button class="btn" onclick="nextQ()">下一题</button>
</div>
