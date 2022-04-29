//js code for battle.html demo
//TODO will need to add data for DEF, SPEED, ETC.

//bookmark: https://www.digitalocean.com/community/tutorials/how-to-use-the-javascript-fetch-api-to-get-data

//attributes of the player's animal
let myJsVariable = JSON.parse(document.getElementById("moves").textContent);
console.log(myJsVariable)

let animal_data = {};
let a_hp_now = 100;
let a_name = "";
//and of the robot
let r_name = ""
let r_atk = 100;
let r_hp = 100;
let r_type = "";
let r_photo = ""

const fetch_data = (url) => {
    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(res => {
            return res.json();
        })
        .then(data => {
            return data;
        });
}

const render_animal = () =>{
    document.getElementById("animal-picked").innerHTML = animal_data['animal_name'];
    document.getElementById("animal-hp-max").innerHTML = animal_data['health']; //starting hp
    document.getElementById("robot-dropdown").disabled = false;
    document.getElementById("animal-photo").src = animal_data['photo_path'];

    document.getElementById("move1").innerHTML = animal_data['move1'];
    document.getElementById("move2").innerHTML = animal_data['move2'];
    document.getElementById("move3").innerHTML = animal_data['move3'];
    document.getElementById("move4").innerHTML = animal_data['move4'];

    var x = document.querySelector('.progress-bar');
    var count = (a_hp_now / animal_data['health']) * 100;
    x.style.width = count + "%";
    x.innerHTML = a_hp_now + "/" + animal_data['health'];
}
//dictate how the html page reacts to data changes
const animal = async () => {

    let a_dd = document.getElementById("animal-dropdown");
    a_name = a_dd.options[a_dd.selectedIndex].text;

    //dictate how to fetch animal battle stats given url of api
    const a_url = "http://127.0.0.1:8000/api/animals/"+a_dd.value+"/?format=json";
    fetch_data(a_url).then(data => {
        animal_data = data;
        render_animal();
    });
};


const robot = async () => {
    let r_dd = document.getElementById("robot-dropdown");
    r_type = r_dd.options[r_dd.selectedIndex].text;

    //dictate how to fetch robot battle stats given url of api
    const r_url = "http://127.0.0.1:8000/api/entities/"+r_dd.value+"/?format=json";
    await fetch(r_url)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let robot = data;
            r_atk = robot['base_atk'];
            r_hp = robot['base_hp'];
            r_name = robot['entity_name']
        })
        .catch((error) => {
            console.log(error);
        });
    document.getElementById("robot-picked").innerHTML = r_type
    document.getElementById("robot-hp").innerHTML = r_hp; //starting hp
    document.getElementById("robot-photo").src = "/static/PseudomonGo/animalimg/"+r_name+".webp";
    document.getElementById("animal-atk").disabled = false;
};

const battle = (action) => {
    /*
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
        document.getElementById("animal-hp-max").innerHTML = a_hp
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
     */
};