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
let current_animal = 0;
let current_robot = 0;


const switch_off = () =>{
    document.getElementById("move1").disabled = true;
    document.getElementById("move2").disabled = true;
    document.getElementById("move3").disabled = true;
    document.getElementById("move4").disabled = true;
    document.getElementById("items").disabled = true;
    document.getElementById("run").disabled = true;

}
const switch_on = () =>{
    document.getElementById("move1").disabled = false;
    document.getElementById("move2").disabled = false;
    document.getElementById("move3").disabled = false;
    document.getElementById("move4").disabled = false;
    document.getElementById("items").disabled = false;
    document.getElementById("run").disabled = false;
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
        this.atk_stage = 0;
        this.def_stage = 0;
        this.spd_stage = 0;
        this.fainted = false;
    }
}
let animals = [];
let robots = [];
let robot_data = {};

let battle_log = "";

const stages = new Map([
    [-6, 0.25],
    [-5, 0.28],
    [-4, 0.33],
    [-3, 0.40],
    [-2, 0.50],
    [-1, 0.66],
    [0, 1],
    [1, 1.5],
    [2, 2],
    [3, 2.5],
    [4, 3],
    [5, 3.5],
    [6, 4],
])

const initialize_battle = () => {
    let animal_list = document.getElementById('animal-dropdown');
    //start at 1 because the first dropdown option is always blank
    for (let i = 0; i < animal_list.length; i++){
        console.log("animals: " + animal_list.options[i].value);
        const a_url = "/api/animals/" + animal_list.options[i].value + "/?format=json";
        fetch_data(a_url).then(data => {
            let animal_data = data;
            animals[i] = new Entity();
            animals[i].name = animal_data['animal_name'];
            animals[i].max_hp = animal_data['health'];
            animals[i].curr_hp = animal_data['health'];
            animals[i].attack = animal_data['attack'];
            animals[i].defense = animal_data['defense'];
            animals[i].speed = animal_data['speed'];
            animals[i].level = animal_data['level'];
            animals[i].photo_path = animal_data['photo_path'];
            let animal_moves = [4];
            animal_moves[0] = animal_data['move1'];
            animal_moves[1] = animal_data['move2'];
            animal_moves[2] = animal_data['move3'];
            animal_moves[3] = animal_data['move4'];
            get_animal_moves(animal_moves, i);
            render_animal();
            current_animal = 0;
            console.log("Created data for animal "+animals[i].name);
            active_animals++;
        });
    }

}
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
    if(type == ANIMAL){
        health_bar = document.querySelectorAll('.progress-bar')[0];
        document.getElementById("animal-hp").innerHTML = curr_hp;
    }
    else if(type == ROBOT){
        health_bar = document.querySelectorAll('.progress-bar')[1];
        document.getElementById("robot-hp").innerHTML = curr_hp;
    }
    let count = (curr_hp / max_hp) * 100;
    health_bar.style.width = count + "%";
    health_bar.innerHTML = curr_hp + "/" + max_hp;
}

const render_animal = () =>{
    document.getElementById("animal-picked").innerHTML = animals[current_animal].name;
    document.getElementById("animal-hp").innerHTML = animals[current_animal].max_hp; //starting hp
    document.getElementById("animal-photo").src = animals[current_animal].photo_path;

    update_health(animals[current_animal], ANIMAL);
}

const render_robot = () => {
    document.getElementById("robot-picked").innerHTML = robots[0].name;
    document.getElementById("robot-hp").innerHTML = robots[0].max_hp; //starting hp
    document.getElementById("robot-photo").src = "/media/images/" + robots[0].name + ".png";

    update_health(robots[0], ROBOT);
}

const render_moves = (move_number) =>{
    if(!animals[current_animal].move_data[move_number]['move_name']){
        animals[current_animal].move_data[move_number]['move_name'] = 'None';
    }
    switch(move_number){
        case 0:
            document.getElementById("move1").innerHTML = animals[current_animal].move_data[0]['move_name'];
            break;
        case 1:
            document.getElementById("move2").innerHTML = animals[current_animal].move_data[1]['move_name'];
            break;
        case 2:
            document.getElementById("move3").innerHTML = animals[current_animal].move_data[2]['move_name'];
            break;
        case 3:
            document.getElementById("move4").innerHTML = animals[current_animal].move_data[3]['move_name'];
            break;
    }
}

const get_animal_moves = (move_ids, index) => {
    for (let i = 0; i < 4; i++){
        const a_url = "/api/moves/" + move_ids[i] + "/?format=json";
        fetch_data(a_url).then(data => {
            animals[index].move_data[i] = data;
            console.log(animals[index].move_data[i]);
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
const switch_animal = async () => {
    switch_on();
    let a_dd = document.getElementById("animal-dropdown");
    //dictate how to fetch animal battle stats given url of api
    update_log(animals[current_animal].name + " switch out!");
    const picked = a_dd.selectedIndex;
    current_animal = picked;
    await sleep(1000);
    update_log("Go " + animals[current_animal].name + "!");
    render_animal();
    battle(6);
};

const calc_robot_stats = (hp, atk, def, spd, lvl) => {
    let bot_hp = Math.floor(0.01 * (2 * hp) * lvl) + lvl + 10;
    let bot_atk = Math.floor(0.01 * (2 * atk) * lvl) + 5;
    let bot_def = Math.floor(0.01 * (2 * def) * lvl) + 5;
    let bot_spd = Math.floor(0.01 * (2 * spd) * lvl) + 5;
    robots[0].max_hp = bot_hp;
    robots[0].curr_hp = bot_hp;
    robots[0].attack = bot_atk;
    robots[0].defense = bot_def;
    robots[0].speed = bot_spd;
}

const robot = async () => {
    let r_dd = document.getElementById("robot-dropdown");

    //dictate how to fetch robot battle stats given url of api
    const r_url = "/api/entities/"+r_dd.value+"/?format=json";

    fetch_data(r_url).then(data => {
        robot_data = data;
        robots[0] = new Entity();
        robots[0].name = robot_data['entity_name'];
        calc_robot_stats(robot_data['base_hp'], robot_data['base_atk'], robot_data['base_def'], robot_data['base_spd'],
            animals[current_animal].level);
        robots[0].level = animals[current_animal].level;
        robots[0].photo_path = robot_data['photo_path'];
        render_robot();
        get_robot_moves();
        document.getElementById("animal-dropdown").disabled = false;
        switch_on();
    });
};


const calc_damage = (move, attacker, target) =>{
    let base_dmg = move['base_damage'];
    let level = attacker.level;
    let atk = attacker.attack * stages.get(attacker.atk_stage);
    let def = target.defense * stages.get(target.def_stage);
    let random = (Math.floor(Math.random() * (100 - 85 + 1) + 85))/100
    let damage = ((((2 * level)/5)+2)*(atk/def)*base_dmg)/50;
    damage *= random;
    console.log(damage);
    return Math.ceil(damage);
}

const edit_stats = (move, target) =>{
    if(target.atk_stage == 6 || target.atk_stage == -6){
        update_log(target.name + "'s Attack cannot be changed any further");
        return;
    }
    if (target.def_stage == 6 || target.def_stage == -6) {
        update_log(target.name + "'s Defense cannot be changed any further");
        return;
    }
    if (target.spd_stage == 6 || target.spd_stage == -6) {
        update_log(target.name + "'s Speed cannot be changed any further");
        return;
    }

    target.atk_stage += move['atk_stage'];
    target.def_stage += move['def_stage'];
    target.spd_stage += move['spd_stage'];

    if (move['atk_stage'] > 0) {
        update_log(target.name + "'s Attack Rose!");
    }
    if (move['def_stage'] > 0) {
        update_log(target.name + "'s Defense Rose!");
    }
    if (move['spd_stage'] > 0) {
        update_log(target.name + "'s Speed Rose!");
    }
    if (move['atk_stage'] < 0) {
        update_log(target.name + "'s Attack Fell!");
    }
    if (move['def_stage'] < 0) {
        update_log(target.name + "'s Defense Fell!");
    }
    if (move['spd_stage'] < 0) {
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
    let hit = Math.floor(Math.random() * 100);
    let move_log = "<b>" + attacker.name +
        " used " + move['move_name'] + "!" + "</b>";
    update_log(move_log);
    if (hit > move.accuracy) {
        update_log("But it missed");
        return;
    }
    if (move['base_damage'] > 0) {
        let damage = calc_damage(move, attacker, target);
        target.curr_hp -= damage;
        if(target.curr_hp < 0){
            target.curr_hp = 0;
        }
        update_health(target, attacker_type ^ 1);
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
        document.getElementById("status").innerHTML = faint_msg;
        update_log(faint_msg);
        target.fainted = true;
        //checks if recently deceased entity is the animal that's out
        if(animals[current_animal].fainted == true){
            document.getElementById("animal-dropdown")[current_animal].disabled = true;
        }
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
    switch_off();
    let animal_spd = animals[current_animal].speed * stages.get(animals[current_animal].spd_stage);
    let robot_spd = robots[0].speed * stages.get(robots[0].spd_stage);
    switch(action){
        case 4:
            console.log("Items!");
            break;
        case 5:
            console.log("Run!");
            break;
        case 6:
            console.log("Switched out!")
            break;
        default:
            if(animal_spd > robot_spd){
                dictate_target(animals[current_animal].move_data[action], animals[current_animal], robots[0], ANIMAL);
                if(check_win(animals[current_animal], robots[0])){
                    return;
                }
                await sleep(1000);
                dictate_target(robots[0].move_data[robot_action], robots[0], animals[current_animal], ROBOT);
                if (check_win(robots[0], animals[current_animal])) {
                    return;
                }
            }
            else if(animal_spd < robot_spd){
                dictate_target(robots[0].move_data[robot_action], robots[0], animals[current_animal], ROBOT);
                if(check_win(robots[0], animals[current_animal]))
                {
                    return;
                }
                await sleep(1000);
                dictate_target(animals[current_animal].move_data[action], animals[current_animal], robots[0], ANIMAL);
                if (check_win(animals[current_animal], robots[0])) {
                    return;
                }
            }
            switch_on();
            return;
    }
    await sleep(1000);
    dictate_target(robots[0].move_data[robot_action], robots[0], animals[current_animal], ROBOT);
    console.log(robot_action);
    switch_on();
};
initialize_battle();