console.log("script load success ");

document.addEventListener("DOMContentLoaded",()=>{

    document.getElementById('add-more-btn').addEventListener('click', function() {
        const container = document.getElementById('json-attributes-container');
        const newRow = document.createElement('div');
        newRow.className = 'json-row';
        newRow.innerHTML = `
            <input type="text" name="json_keys[]" placeholder="Key">
            <input type="text" name="json_values[]" placeholder="Value">
            
        `;
        container.appendChild(newRow);
    });



})