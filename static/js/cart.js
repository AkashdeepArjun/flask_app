document.addEventListener("DOMContentLoaded",()=>{

    console.log("script load success ")


    window.handle_logic = async function (){

        
        try {

            const http_response = await fetch(`place_order`,{method:"POST"})

            if(http_response.ok){

                const json_response = await http_response.json()

                console.log(`response is ${json_response}`)



            }





            
        } catch (error) {
            
            alert(`error occured :${error} `)
        }





    }




})