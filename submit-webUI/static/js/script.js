async function handleCalc() {
    const input_text_A = document.getElementById("input_text").value;
    const response = await fetch('/translate', {
        method: 'POST',
        body: new FormData(document.querySelector('form')),
        headers: {
            'Accept': 'application/json'
        }
    });
    const data = await response.json();
    document.getElementById("output_text").value = data.output;
}

async function handleClear() {
    document.getElementById("input_text").value = '';
    document.getElementById("output_text").value = '';
}

document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start_button');
    const resetButton = document.getElementById('reset_button');

    startButton.addEventListener('click', handleCalc);
    resetButton.addEventListener('click', handleClear);
});
