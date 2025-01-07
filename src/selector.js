// Create a selector for the progress bar and the draggable dot

export function createSelector(ticks, onChange) {

    // Helper function to snap the dot to the nearest tick
    function snapToTick(position) {
        return Math.round(position / tickWidth) * tickWidth;
    }

    // Helper function to trigger a change event
    function triggerChangeEvent(value) {
        onChange(value);
    }

    const numTicks = ticks.length;

    const selector = document.createElement('div');
    selector.style.position = 'relative';
    selector.style.width = '300px'; // Width of the progress bar
    selector.style.height = '10px'; // Height of the progress bar
    selector.style.backgroundColor = '#e0e0e0';
    selector.style.borderRadius = '5px';
    selector.style.margin = '0px auto 100px auto';
    selector.style.cursor = 'pointer';

    const actualWidth = 300-20;

    const tickWidth = (actualWidth) / (numTicks - 1);

    // Create the draggable dot
    const dot = document.createElement('div');
    dot.style.position = 'absolute';
    dot.style.top = '-5px';
    dot.style.left = (numTicks - 1) * tickWidth + 'px';
    dot.style.width = '20px';
    dot.style.height = '20px';
    dot.style.backgroundColor = '#007BFF';
    dot.style.borderRadius = '50%';
    dot.style.cursor = 'grab';
    dot.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';

    // create placeholder dots
    for(let i = 0; i < numTicks; i++){
        const greydot = document.createElement('div');
        greydot.style.position = 'absolute';
        greydot.style.top = '-5px';
        greydot.style.left = i * tickWidth + 'px';
        greydot.style.width = '20px';
        greydot.style.height = '20px';
        greydot.style.backgroundColor = '#e0e0e0';
        greydot.style.borderRadius = '50%';
        greydot.style.cursor = 'pointer';
        //greydot.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';
        selector.appendChild(greydot);

        const label = document.createElement('p');
        label.style.position = 'absolute';
        label.style.top = '10px';
        label.style.left = i * tickWidth + 'px';
        label.style.fontSize = 'small';
        label.innerHTML = ticks[i];

        selector.appendChild(label);

        greydot.addEventListener("click", (event) => {
            event.preventDefault();
            isDragging = false;

            const oldLeftPx = dot.style.left;

            const newLeft = i * tickWidth;

            const newLeftPx = `${newLeft}px`;

            if (newLeftPx != oldLeftPx) {
                dot.style.left = newLeftPx;

                // Calculate the progress value (0 to 100)
                const value = Math.round((newLeft / actualWidth) * 100);

                triggerChangeEvent(value);
            }
        });

    }

    
    selector.appendChild(dot);

    // Draggable logic
    let isDragging = false;
    dot.addEventListener('mousedown', (event) => {
        event.preventDefault();
        isDragging = true;
        dot.style.cursor = 'grabbing';
    });

    window.addEventListener('mousemove', (event) => {
        if (!isDragging) return;

        const rect = selector.getBoundingClientRect();

        let newLeft = event.clientX - rect.left;

        // Constrain within progress bar boundaries
        newLeft = Math.max(0, Math.min(newLeft, actualWidth));

        // Snap to nearest tick
        newLeft = snapToTick(newLeft);

        const oldLeftPx = dot.style.left;

        const newLeftPx = `${newLeft}px`;

        if (newLeftPx != oldLeftPx) {
            dot.style.left = newLeftPx;

            // Calculate the progress value (0 to 100)
            const value = Math.round((newLeft / actualWidth) * 100);

            triggerChangeEvent(value);
        }
            
    });

    window.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            dot.style.cursor = 'grab';
        }
    });

    return selector;
}
