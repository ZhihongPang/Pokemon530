//js code for battle.html demo
//TODO will need to add data for DEF, SPEED, ETC.

//bookmark: https://www.digitalocean.com/community/tutorials/how-to-use-the-javascript-fetch-api-to-get-data

//attributes of the player's animal
let myJsVariable = JSON.parse(document.getElementById("moves").textContent);
console.log(myJsVariable)

const ANIMAL = 0;
const ROBOT = 1;
let active_robots = 0;
let active_animals = 0;


const switch_buttons = () =>{
    console.log("Switching Buttons");
    if(document.getElementById("move1").disabled == true){
        document.getElementById("move1").disabled = false;
        document.getElementById("move2").disabled = false;
        document.getElementById("move3").disabled = false;
        document.getElementById("move4").disabled = false;
        document.getElementById("items").disabled = false;
        document.getElementById("run").disabled = false;
    }
    else{
        document.getElementById("move1").disabled = true;
        document.getElementById("move2").disabled = true;
        document.getElementById("move3").disabled = true;
        document.getElementById("move4").disabled = true;
        document.getElementById("items").disabled = true;
        document.getElementById("run").disabled = true;
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

class Entity {
    constructor(name, max_hp, curr_hp, attack, defense, speed, level, photo_path, move_data=[]) {
        this.name = name;
        this.max_hp = max_hp;
        this.curr_hp = curr_hp;
        this.attack = attack;
        this.defense = defense;
        this.speed = speed;
        this.level = level;
        this.photo_path = photo_path;
        this.move_data = move_data;
    }
}
let animals = [];
let robots = [];
let animal_data = {};
let robot_data = {};

let battle_log = "";
//and of the robot

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
const update_health = (entity, type) =>{
    let max_hp = entity.max_hp;
    let curr_hp = entity.curr_hp;

    let health_bar;
    if(type == ROBOT){
        health_bar = document.querySelectorAll('.progress-bar')[0];
        document.getElementById("animal-hp").innerHTML = curr_hp;
    }
    else if(type == ANIMAL){
        health_bar = document.querySelectorAll('.progress-bar')[1];
        document.getElementById("robot-hp").innerHTML = curr_hp;
    }
    let count = (curr_hp / max_hp) * 100;
    health_bar.style.width = count + "%";
    health_bar.innerHTML = curr_hp + "/" + max_hp;
}

const render_animal = () =>{
    document.getElementById("animal-picked").innerHTML = animals[0].name;
    document.getElementById("animal-hp").innerHTML = animals[0].max_hp; //starting hp
    document.getElementById("robot-dropdown").disabled = false;
    document.getElementById("animal-photo").src = animals[0].photo_path;

    let animal_moves = [4];
    animal_moves[0] = animal_data['move1'];
    animal_moves[1] = animal_data['move2'];
    animal_moves[2] = animal_data['move3'];
    animal_moves[3] = animal_data['move4'];
    get_animal_moves(animal_moves);
    update_health(animals[0], ANIMAL);
}

const render_robot = () => {
    document.getElementById("robot-picked").innerHTML = robots[0].name;
    document.getElementById("robot-hp").innerHTML = robots[0].max_hp; //starting hp
    document.getElementById("robot-photo").src = "/media/images/" + robots[0].name + ".webp";

    update_health(robots[0], ROBOT);
}

const render_moves = (move_number) =>{
    if(!animals[0].move_data[move_number]['move_name']){
        animals[0].move_data[move_number]['move_name'] = 'None';
    }
    switch(move_number){
        case 0:
            document.getElementById("move1").innerHTML = animals[0].move_data[0]['move_name'];
            break;
        case 1:
            document.getElementById("move2").innerHTML = animals[0].move_data[1]['move_name'];
            break;
        case 2:
            document.getElementById("move3").innerHTML = animals[0].move_data[2]['move_name'];
            break;
        case 3:
            document.getElementById("move4").innerHTML = animals[0].move_data[3]['move_name'];
            break;
    }
}

const get_animal_moves = (move_ids) => {
    for (let i = 0; i < 4; i++){
        const a_url = "/api/moves/" + move_ids[i] + "/?format=json";
        fetch_data(a_url).then(data => {
            animals[0].move_data[i] = data;
            console.log(animals[0].move_data[i]);
            render_moves(i);
        });
    }
}

const get_robot_moves = () => {
    let i = 0;
    while(robot_data['moves'][i]){
        robots[0].move_data[i] = robot_data['moves'][i];
        console.log(robots[0].move_data[i]);
        i++;
    }
}

//dictate how the html page reacts to data changes
const animal = async () => {

    let a_dd = document.getElementById("animal-dropdown");

    //dictate how to fetch animal battle stats given url of api
    const a_url = "/api/animals/"+a_dd.value+"/?format=json";
    fetch_data(a_url).then(data => {
        console.log(data);
        animal_data = data;
        animals[0] = new Entity();
        animals[0].name = animal_data['animal_name'];
        animals[0].max_hp = animal_data['health'];
        animals[0].curr_hp = animal_data['health'];
        animals[0].attack = animal_data['attack'];
        animals[0].defense = animal_data['defense'];
        animals[0].speed = animal_data['speed'];
        animals[0].level = animal_data['level'];
        animals[0].photo_path = animal_data['photo_path'];
        render_animal();
    });
};


const robot = async () => {
    let r_dd = document.getElementById("robot-dropdown");

    //dictate how to fetch robot battle stats given url of api
    const r_url = "/api/entities/"+r_dd.value+"/?format=json";

    fetch_data(r_url).then(data => {
        robot_data = data;
        robots[0] = new Entity();
        robots[0].name = robot_data['entity_name'];
        robots[0].max_hp = robot_data['base_hp'];
        robots[0].curr_hp = robot_data['base_hp'];
        robots[0].attack = robot_data['base_atk'];
        robots[0].defense = robot_data['base_def'];
        robots[0].speed = robot_data['base_spd'];
        robots[0].level = animal_data['level'];
        robots[0].photo_path = robot_data['photo_path'];
        render_robot();
        get_robot_moves();
    });
    switch_buttons();
};

const calc_damage = (move, attacker, target) =>{
    let base_dmg = move['base_damage'];
    let level = attacker.level;
    let atk = attacker.attack;
    let def = target.defense;
    let damage = ((((2 * level)/5)+2)*(atk/def)*base_dmg)/50;
    console.log(damage);
    return Math.ceil(damage);
}


const edit_stats = (move, target) =>{
    target.attack *= move['atk_multiplier'];
    target.defense *= move['def_multiplier'];
    target.speed *= move['spd_multiplier'];

    if (move['atk_multiplier'] > 1) {
        update_log(target.name + "'s Attack Rose!");
    }
    if (move['def_multiplier'] > 1) {
        update_log(target.name + "'s Defense Rose!");
    }
    if (move['spd_multiplier'] > 1) {
        update_log(target.name + "'s Speed Rose!");
    }
    if (move['atk_multiplier'] < 1) {
        update_log(target.name + "'s Attack Fell!");
    }
    if (move['def_multiplier'] < 1) {
        update_log(target.name + "'s Defense Fell!");
    }
    if (move['spd_multiplier'] < 1) {
        update_log(target.name + "'s Speed Fell!");
    }
}
const dictate_target = (move, attacker, target, attacker_type) => {
    if(move['target'] == 'O'){
        make_move(move, attacker, target, attacker_type);
    } else if (move['target'] == 'S') {
        make_move(move, attacker, attacker, attacker_type);
    }
}

const make_move = (move, attacker, target, attacker_type) =>{
    let move_log = "<b>" + attacker.name +
        " used " + move['move_name'] + "!" + "</b>";
    update_log(move_log);
    if (move['base_damage'] > 0) {
        let damage = calc_damage(move, attacker, target);
        target.curr_hp -= damage;
        if(target.curr_hp < 0){
            target.curr_hp = 0;
        }
        update_health(target, attacker_type);
        update_log(target.name + " took " + damage + " damage!");
    }
    edit_stats(move, target);
}

const update_log = (message) => {
    document.getElementById("status").innerHTML = message + '<br>';
    battle_log = battle_log.concat(message + '<br>');
    document.getElementById("battle_log").innerHTML = battle_log;
}

const check_win = (attacker, target) => {
    if(target.curr_hp == 0){
        let faint_msg = target.name + ' fainted!' + '<br>';
        document.getElementById("status").innerHTML = faint_msg
        update_log(faint_msg);
        return true;
    }
    else{
        return false;
    }
}

/* 0 - Move 1
*  1 - Move 2
*  2 - Move 3
*  3 - Move 4
*  4 - Item
*  5 - Run
*/
const battle = async(action) => {
    let robot_action = Math.floor(Math.random() * robots[0].move_data.length);
    console.log(action);
    switch(action){
        case 4:
            console.log("Items!");
            break;
        case 5:
            console.log("Run!");
            break;
        default:
            switch_buttons();
            if(animals[0].speed > robots[0].speed){
                dictate_target(animals[0].move_data[action], animals[0], robots[0], ANIMAL);
                if(check_win(animals[0], robots[0])){
                    return;
                }
                await sleep(1000);
                dictate_target(robots[0].move_data[robot_action], robots[0], animals[0], ROBOT);
                if (check_win(robots[0], animals[0])) {
                    return;
                }
            }
            else if(animals[0].speed < robots[0].speed){
                dictate_target(robots[0].move_data[robot_action], robots[0], animals[0], ROBOT);
                if(check_win(robots[0], animals[0]))
                {
                    return;
                }
                await sleep(1000);
                dictate_target(animals[0].move_data[action], animals[0], robots[0], ANIMAL);
                if (check_win(animals[0], robots[0])) {
                    return;
                }
            }
            switch_buttons();
            return;
    }
    await sleep(1000);
    dictate_target(robots[0].move_data[robot_action], robots[0], animals[0], ROBOT);
    console.log(robot_action);
    switch_buttons();
};