//js code for battle.html demo
//TODO will need to add data for DEF, SPEED, ETC.

//bookmark: https://www.digitalocean.com/community/tutorials/how-to-use-the-javascript-fetch-api-to-get-data

//attributes of the player's animal
let myJsVariable = JSON.parse(document.getElementById("moves").textContent);
console.log(myJsVariable)

let animal_data = {};
let robot_data = {};
let a_hp_now = 50;
let a_name = "";
let move_data = [];
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

    let animal_moves = [4];
    animal_moves[0] = animal_data['move1'];
    animal_moves[1] = animal_data['move2'];
    animal_moves[2] = animal_data['move3'];
    animal_moves[3] = animal_data['move4'];
    moves(animal_moves);

    let x = document.querySelector('.progress-bar');
    let count = (a_hp_now / animal_data['health']) * 100;
    x.style.width = count + "%";
    x.innerHTML = a_hp_now + "/" + animal_data['health'];
}

const render_moves = (move_number) =>{
    if(!move_data[move_number]['move_name']){
        move_data[move_number]['move_name'] = 'None';
    }
    switch(move_number){
        case 0:
            document.getElementById("move1").innerHTML = move_data[0]['move_name'];
            break;
        case 1:
            document.getElementById("move2").innerHTML = move_data[1]['move_name'];
            break;
        case 2:
            document.getElementById("move3").innerHTML = move_data[2]['move_name'];
            break;
        case 3:
            document.getElementById("move4").innerHTML = move_data[3]['move_name'];
            break;
    }
}

const moves = (move_ids) => {
    for (let i = 0; i < 4; i++){
        const a_url = "http://127.0.0.1:8000/api/moves/" + move_ids[i] + "/?format=json";
        fetch_data(a_url).then(data => {
            move_data[i] = data;
            console.log(move_data[i]);
            render_moves(i);
        });
    }
}

//dictate how the html page reacts to data changes
const animal = async () => {

    let a_dd = document.getElementById("animal-dropdown");
    a_name = a_dd.options[a_dd.selectedIndex].text;

    //dictate how to fetch animal battle stats given url of api
    const a_url = "http://127.0.0.1:8000/api/animals/"+a_dd.value+"/?format=json";
    fetch_data(a_url).then(data => {
        console.log(data);
        animal_data = data;
        render_animal();
    });
};


const robot = async () => {
    let r_dd = document.getElementById("robot-dropdown");
    r_type = r_dd.options[r_dd.selectedIndex].text;

    //dictate how to fetch robot battle stats given url of api
    const r_url = "http://127.0.0.1:8000/api/entities/"+r_dd.value+"/?format=json";

    fetch_data(r_url).then(data => {
        robot_data = data;
        document.getElementById("robot-picked").innerHTML = robot_data['entity_name']
        document.getElementById("robot-hp").innerHTML = robot_data['base_hp']; //starting hp
        document.getElementById("robot-photo").src = "http://127.0.0.1:8000/media/images/" + robot_data['entity_name']+ ".webp";
    });
};

const make_move = (move_num) =>{
    
}

/* 0 - Move 1
*  1 - Move 2
*  2 - Move 3
*  3 - Move 4
*  4 - Item
*  5 - Run
*/
const battle = (action) => {
    console.log(action);
    switch(action){
        case 4:
            console.log("Items!");
            break;
        case 5:
            console.log("Run!");
            break;
        default:
            make_move(action);
            console.log("Move")
    }
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