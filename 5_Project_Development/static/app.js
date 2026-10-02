const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const inputLabel = document.getElementById("inputLabel");
const questionCount = document.getElementById("questionCount");
const quizOptions = document.getElementById("quizOptions");
const submitButton = document.getElementById("submitButton");
const statusText = document.getElementById("status");
const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");
const copyButton = document.getElementById("copyButton");

const taskInfo = {
    qa: {
        label: "Your question",
        placeholder: "Example: Which is the largest ocean?",
        button: "Answer Question"
    },
    explain: {
        label: "Topic to explain",
        placeholder: "Example: Explain the Pythagoras theorem simply.",
        button: "Explain Topic"
    },
    quiz: {
        label: "Quiz topic",
        placeholder: "Example: Generate a quiz about SQL joins.",
        button: "Generate Quiz"
    },
    summarize: {
        label: "Text to summarize",
        placeholder: "Paste your educational paragraph or notes here.",
        button: "Summarize Text"
    },
    recommendations: {
        label: "Topic for learning path",
        placeholder: "Example: I want to learn Python from beginner to advanced.",
        button: "Create Learning Path"
    }
};

function updateTaskUI() {
    const info = taskInfo[task.value];
    inputLabel.textContent = info.label;
    inputText.placeholder = info.placeholder;
    submitButton.textContent = info.button;
    quizOptions.classList.toggle("hidden", task.value !== "quiz");
}

task.addEventListener("change", updateTaskUI);

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderPlainText(text) {
    result.innerHTML = `<div class="answer-text">${escapeHtml(text)}</div>`;
}

function renderQuiz(questions) {
    result.innerHTML = questions.map((item, index) => {
        const options = item.options.map((option) => `
            <button class="quiz-option"
                    data-question="${index}"
                    data-answer="${escapeHtml(item.answer)}"
                    data-option="${escapeHtml(option)}">
                ${escapeHtml(option)}
            </button>
        `).join("");

        return `
            <article class="quiz-question">
                <h3>${index + 1}. ${escapeHtml(item.question)}</h3>
                ${options}
                <p class="quiz-explanation" id="explanation-${index}"></p>
            </article>
        `;
    }).join("");

    document.querySelectorAll(".quiz-option").forEach((button) => {
        button.addEventListener("click", () => {
            const questionIndex = button.dataset.question;
            const answer = button.dataset.answer;
            const selected = button.dataset.option;
            const buttons = document.querySelectorAll(
                `.quiz-option[data-question="${questionIndex}"]`
            );

            buttons.forEach((item) => {
                item.disabled = true;
                if (item.dataset.option === answer) {
                    item.classList.add("correct");
                }
            });

            if (selected !== answer) {
                button.classList.add("wrong");
            }

            const question = questions[Number(questionIndex)];
            document.getElementById(`explanation-${questionIndex}`).textContent =
                selected === answer
                    ? `Correct. ${question.explanation || ""}`
                    : `Correct answer: ${answer}. ${question.explanation || ""}`;
        });
    });
}

async function submitTask() {
    const text = inputText.value.trim();

    if (!text) {
        statusText.textContent = "Please enter some text first.";
        return;
    }

    submitButton.disabled = true;
    statusText.textContent = "EduGenie is thinking...";
    resultCard.classList.add("hidden");
    result.innerHTML = "";

    let endpoint;
    let body;

    if (task.value === "qa") {
        endpoint = "/qa";
        body = { text };
    } else if (task.value === "explain") {
        endpoint = "/explain";
        body = { text };
    } else if (task.value === "quiz") {
        endpoint = "/quiz";
        body = {
            topic: text,
            num_questions: Number(questionCount.value)
        };
    } else if (task.value === "summarize") {
        endpoint = "/summarize";
        body = { text };
    } else {
        endpoint = "/learn/recommendations";
        body = { text };
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed.");
        }

        resultCard.classList.remove("hidden");

        if (task.value === "quiz") {
            renderQuiz(data.result);
        } else {
            renderPlainText(data.result);
        }

        statusText.textContent = "Completed.";
    } catch (error) {
        resultCard.classList.remove("hidden");
        renderPlainText(`Error: ${error.message}`);
        statusText.textContent = "Something went wrong.";
    } finally {
        submitButton.disabled = false;
    }
}

submitButton.addEventListener("click", submitTask);

copyButton.addEventListener("click", async () => {
    const text = result.innerText.trim();
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        copyButton.textContent = "Copied";
        setTimeout(() => {
            copyButton.textContent = "Copy";
        }, 1200);
    } catch {
        copyButton.textContent = "Copy failed";
    }
});

updateTaskUI();
