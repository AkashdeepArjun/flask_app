document.addEventListener("DOMContentLoaded",()=>{

  
console.log("script loaded")

let debounceTimer;
let currentPage = 1;
let hasNextPage = false;
let isLoading = false;
let currentQuery = "";


    
    search_box = document.querySelector('#search_box')

    const suggestionBox = document.getElementById('suggestion-box');
    const suggestionList = document.getElementById('suggestion-list');
    const loadingIndicator = document.getElementById('loading-indicator');


 



    function resetDropdown() {
    suggestionBox.style.display = 'none';
    suggestionList.innerHTML = "";
    hasNextPage = false;
    currentPage = 1;
}

   document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-container')) resetDropdown();
});

    window.handleCartEvent = async function (event,product_id) {

        console.log("function called ")
        event.preventDefault();
        
        qty_input = document.getElementById(`qty-${product_id}`);

        quantity = parseInt(qty_input.value,10);

        if (!quantity || quantity < 1){

            alert("please add valid quantity");
            
            return;

        }

        form = event.target;
        button = form.querySelector("button[type='submit']")
        button.innerText= "Adding..."
        button.disabled=true

        try {

            const http_response= await fetch (`/cart/add`,
            {method:"POST",headers:{"Content-type": "application/json"},
                body: JSON.stringify({
                product_id: product_id,
                quantity: quantity
                })
            } );

            if(http_response.ok) {

                data = await http_response.json()
                qty_input.value=1
                alert("product added successfully")
                button.disabled=false
                button.innerText="Add to Cart"

            }else{

                alert(
                    "unknown error occured"
                )

                button.disabled=false
                button.innerText="Add to Cart"


            }
                

            
        } catch (error) {
            
            alert(` error : ${error}`)
            button.disabled=false
            button.innerText="Add to Cart"
        }



    }




  
    const fetch_suggesions = async(query,page) =>{

        if(isLoading) {
            
            return 
        }

         isLoading = true;
         loadingIndicator.style.display = 'block';






        const http_response = await fetch(`http://127.0.0.1:5000/api/search-suggestions?q=${encodeURIComponent(query)}&page=${page}`)
        
        if(http_response.ok){

            const json_response  = await http_response.json()
            console.log("respose" ,json_response.items)

            if(json_response.items.length ==0  && page==1){

                resetDropdown()

                return



            }
            json_response.items.forEach( item=> {

                  const link = document.createElement('a');
                link.href = `/products/${item.id}`;
                link.textContent = item.name;
                link.style.cssText = "display: block; padding: 10px; text-decoration: none; color: #333; border-bottom: 1px solid #f0f0f0;";
                
                // Optional hover effect
                link.onmouseenter = () => link.style.background = "#f5f5f5";
                link.onmouseleave = () => link.style.background = "transparent";
                
                suggestionList.appendChild(link);

                
            });


            hasNextPage = json_response.has_next;
            suggestionBox.style.display = 'block';
            isLoading = false;
            loadingIndicator.style.display = 'none';







        }






    }


    suggestionBox.addEventListener('scroll', () => {
    // Check if user scrolled near the bottom of the 250px container
    const triggerThreshold = suggestionBox.scrollHeight - suggestionBox.scrollTop <= suggestionBox.clientHeight + 20;
    
    if (triggerThreshold && hasNextPage && !isLoading) {
        currentPage++;
        fetchSuggestions(currentQuery, currentPage);
    }
});



   
    search_box.addEventListener("input",()=>{

    clearTimeout(debounceTimer);
    const query = search_box.value.trim();

    if (query.length < 2) {
        resetDropdown();
        return;
    }


        debounceTimer = setTimeout(() => {
        currentQuery = query;
        currentPage = 1; // Reset to page 1 for a brand new search term
        suggestionList.innerHTML = ""; // Wipe old results
        fetch_suggesions(currentQuery, currentPage);
    }, 500);



    })


    
    


    







})