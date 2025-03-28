document.addEventListener('DOMContentLoaded', function() {
    const classifyBtn = document.getElementById('classify-btn');
    const textInput = document.getElementById('text-input');
    const resultSection = document.querySelector('.result-section');
    const originalText = document.getElementById('original-text');
    const intentResult = document.getElementById('intent');
    const confidenceResult = document.getElementById('confidence');
    const exampleBtns = document.querySelectorAll('.example-btn');

    // Classify button click handler
    classifyBtn.addEventListener('click', async function() {
        const text = textInput.value.trim();
        console.log('Classifying text:', text);

        if (!text) {
            alert('Please enter some text to classify');
            return;
        }

        // Show loading state
        classifyBtn.disabled = true;
        classifyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        resultSection.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `text=${encodeURIComponent(text)}`
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            console.log('Classification result:', data);

            // Display results
            originalText.textContent = data.text;
            intentResult.textContent = `${data.intent} (Class ${data.class_id})`;
            confidenceResult.textContent = `${(data.confidence * 100).toFixed(2)}%`;
            
            // Add intent-specific styling
            intentResult.className = 'value intent-value';
            intentResult.classList.add(`intent-${data.class_id}`);
            
            resultSection.classList.remove('hidden');

        } catch (error) {
            console.error('Classification failed:', error);
            alert(`Error: ${error.message}`);
        } finally {
            classifyBtn.disabled = false;
            classifyBtn.innerHTML = '<i class="fas fa-search"></i> Classify';
        }
    });

    // Example buttons handler
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            textInput.value = this.textContent;
            textInput.focus();
        });
    });

    // Allow Enter key submission
    textInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            classifyBtn.click();
        }
    });
});