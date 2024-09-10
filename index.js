
function rollDice(){
    const numofDice = document.getElementById("numOfDice").value;
    const diceresult = document.getElementById("diceResult");
    const diceImage = document.getElementById("diceImages");
    const values =[];
    const images = [];

    for(let i = 0; i < numofDice; i ++){
        const randnum = Math.floor(Math.random() *6) + 1;
        values.push(randnum); //append randnum into values list
        images.push(`<img src="Dice/Dice-${randnum}.png" alt = "Dice ${randnum}">`); 
    } //alt will be excused in case of the file name is wrong
    diceresult.textContent = `dice: ${values.join(", ")}`; 

    diceImage.innerHTML = images.join(""); //images
}
console.log("Hello");

