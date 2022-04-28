//js code for battle.html demo
//TODO will need to add data for DEF, SPEED, ETC.

//bookmark: https://www.digitalocean.com/community/tutorials/how-to-use-the-javascript-fetch-api-to-get-data

//attributes of the player's animal
let a_atk = 100;
let a_hp = 100;
let a_name = "";
//and of the robot
let r_atk = 100;
let r_hp = 100;
let r_type = "";

//dictate how the html page reacts to data changes
const animal = async () => {
    let a_dd = document.getElementById("animal-dropdown");
    a_name = a_dd.options[a_dd.selectedIndex].text;
    document.getElementById("animal-picked").innerHTML = a_name;
    document.getElementById("animal-hp").innerHTML = a_hp; //starting hp
    document.getElementById("robot-dropdown").disabled = false;

    //dictate how to fetch animal battle stats given url of api
    const a_url = "http://127.0.0.1:8000/api/animals/"+a_dd.value+"/?format=json";
    console.log(a_url);
    await fetch(a_url)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let animal = data;
            a_atk = animal['attack'];
            a_hp = animal['health'];
        })
        .catch((error) => {
            console.log(error);
        });
};

const robot = async () => {
    let r_dd = document.getElementById("robot-dropdown");
    r_type =r_dd.options[r_dd.selectedIndex].text;
    document.getElementById("robot-picked").innerHTML = r_type
    document.getElementById("robot-hp").innerHTML = r_hp; //starting hp
    document.getElementById("animal-atk").disabled = false;

    //dictate how to fetch robot battle stats given url of api
    const r_url = "http://127.0.0.1:8000/api/robots/"+r_dd.value+"/?format=json";
    await fetch(r_url)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let robot = data;
            r_atk = robot['attack'];
            r_hp = robot['health'];
        })
        .catch((error) => {
            console.log(error);
        });
};

const battle = () => {
    const responses = [
        `${a_name} inflicted ${a_atk} dmg`,
        `${r_type} inflicted ${r_atk} dmg`,
    ]
    //calculate animals' dmg versus robot's hp
    r_hp -= a_atk;
    setTimeout(() => {
        alert(responses[0]);
        document.getElementById("status").innerHTML = responses[0];
        document.getElementById("robot-hp").innerHTML = r_hp;
    });
    //same thing as above but for robot to player's animal
    a_hp -= r_atk;
    setTimeout(() => {
        alert(responses[1]);
        document.getElementById("status").innerHTML = responses[1];
        document.getElementById("animal-hp").innerHTML = a_hp
    }, 1500);
    //win condition
    if(a_hp <= 0 || r_hp <= 0) {
        let winner = "";
        if(a_hp <= 0) {
            winner = `${r_type}`;
        } else {
            winner = `${a_name}`;
        }
        document.getElementById("winner").innerHTML = "Winner 🎉: " + winner;
        document.getElementById("animal-atk").disabled = true;
    }
};