//js code for battle.html demo
//TODO will need to add data for DEF, SPEED, ETC.

//bookmark: https://www.digitalocean.com/community/tutorials/how-to-use-the-javascript-fetch-api-to-get-data

//attributes of the player's animal
let myJsVariable = JSON.parse(document.getElementById("moves").textContent);
console.log(myJsVariable)

let animal_data = {};
let robot_data = {};
let a_hp_now = 0;
let a_name = "";
let move_data = [];
let battle_log = "";
//and of the robot
let r_name = ""
let r_atk = 100;
let r_hp = 100;
let r_hp_now = 100;
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
const update_a_health = () =>{
    if(a_hp_now < 0){
        a_hp_now = 0;
    }
    let animal_health = document.querySelectorAll('.progress-bar')[0];
    let count = (a_hp_now / animal_data['health']) * 100;
    animal_health.style.width = count + "%";
    animal_health.innerHTML = a_hp_now + "/" + animal_data['health'];
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
    a_hp_now = animal_data['health'];
    update_a_health();
}

const update_r_health = () => {
    if(r_hp_now < 0){
        r_hp_now = 0;
    }
    let robot_health = document.querySelectorAll('.progress-bar')[1];
    let count = (r_hp_now / robot_data['base_hp']) * 100;
    robot_health.style.width = count + "%";
    robot_health.innerHTML = r_hp_now + "/" + robot_data['base_hp'];
}

const render_robot = () => {
    document.getElementById("robot-picked").innerHTML = robot_data['entity_name']
    document.getElementById("robot-hp").innerHTML = robot_data['base_hp']; //starting hp
    document.getElementById("robot-photo").src = "http://127.0.0.1:8000/media/images/" + robot_data['entity_name'] + ".webp";

    update_r_health();
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
        r_hp_now = robot_data['base_hp']
        render_robot();
    });
};

const make_move = (move_num, attacker_atk, defender_def, level) =>{
    let damage1 = (((2 * level)/5)+2);
    let damage2 = move_data[move_num]['base_damage'];
    let damage3 = attacker_atk/defender_def;
    let damage = damage1*damage2*damage3/50;
    console.log(damage);
    return Math.ceil(damage);
}

const update_log = (message) => {
    document.getElementById("status").innerHTML = message + '<br>';
    battle_log = battle_log.concat(message + '<br>');
    document.getElementById("battle_log").innerHTML = battle_log;
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
            let move_log ="<b>"+animal_data['animal_name'] +
                " used " + move_data[action]['move_name'] + "!" +"</b>";
            update_log(move_log);
            if(move_data[action]['base_damage'] > 0){
                let damage = make_move(action, animal_data['attack'], robot_data['base_def'], animal_data['level']);
                r_hp_now -= damage;
                update_r_health();
                update_log(robot_data['entity_name'] + " took " + damage + " damage!");
            }
            if(move_data[action]['atk_multiplier'] != 1){
                robot_data['base_atk'] *= move_data[action]['atk_multiplier'];
                update_log(robot_data['entity_name'] + "'s Attack Fell!");
            }
            if (move_data[action]['def_multiplier'] != 1) {
                robot_data['base_def'] *= move_data[action]['def_multiplier'];
                update_log(robot_data['entity_name'] + "'s Defense Fell!");
            }
            if (move_data[action]['spd_multiplier'] != 1) {
                robot_data['base_spd'] *= move_data[action]['spd_multiplier'];
                update_log(robot_data['entity_name'] + "'s Speed Fell!");
            }
    }

};