// Object Oriented Pragraming ---> Way of Writing Code 

class BankAcount{
    #balance = 0;

    deposit(amount){
        this.#balance+=amount;
        return this.#balance
    }

    getBalance(){
        return `${this.#balance}`
    }
}

let account = new BankAcount()

account.balance
console.log(account.getBalance());

// DOM Manipulation 

// Promises In JS
function  fetch_data(){
    return new Promise((resolve,reject) => {
        setTimeout(() =>{
            let sucess = true
            if (sucess){
                resolve("Data Fetched Sucessfully ")
            } else{
                reject("Error Fetching Data")
            }
        },3000)
    })
}

let response = fetch_data()
console.log(response);
