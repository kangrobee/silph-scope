
CREATE TABLE IF NOT EXISTS pokemon (
    pokemon_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER
);

CREATE TABLE IF NOT EXISTS species (
    species_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS abilities (
    ability_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    generation TEXT
);

CREATE TABLE IF NOT EXISTS moves (
    move_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    generation TEXT,
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    priority INTEGER
);

CREATE TABLE IF NOT EXISTS berries (
    berry_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS egg_groups (
    egg_group_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_conds (
    encounter_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_values (
    encounter_value_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encounter_methods (
    encounter_method_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS evolution_chains (
    evolution_chain_id INTEGER PRIMARY KEY,
    evolution_chain_id2 INTEGER
);

CREATE TABLE IF NOT EXISTS evolution_triggers (
    evolution_trigger_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS genders (
    gender_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS generations (
    generation_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS growth_rates (
    growth_rate_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cost INTEGER,
    fling_power INTEGER
);

CREATE TABLE IF NOT EXISTS item_attributes (
    item_attribute_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_categories (
    item_category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_fling_effects (
    item_fling_effect_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS item_pockets (
    item_pocket_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS location_areas (
    location_area_id INTEGER PRIMARY KEY,
    location_name TEXT NOT NULL,
    name TEXT
);


CREATE TABLE IF NOT EXISTS machines (
    machine_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    move_name TEXT
);

CREATE TABLE IF NOT EXISTS move_ailments (
    move_ailment_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_battle_styles (
    move_battle_style_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_categories(
    move_category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_damage_classes (
    move_damage_class_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS move_learn_methods (
    move_learn_method_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS move_targets (
    move_target_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS natures (
    nature_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    decreased_stat TEXT,
    increased_stat TEXT
);

CREATE TABLE IF NOT EXISTS pokedexes (
    pokedex_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS colors (
    color_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shapes (
    shape_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS habitats (
    habitat_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stats (
    stat_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS versions (
    version_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS version_groups (
    version_group_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    order_num INTEGER
);


CREATE TABLE IF NOT EXISTS pokemon_abilities (
    pokemon_id INTEGER,
    ability_id INTEGER,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (ability_id) REFERENCES abilities(ability_id)
);


CREATE TABLE IF NOT EXISTS pokemon_types (
    pokemon_id INTEGER,
    type_id INTEGER,
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (type_id) REFERENCES types(type_id)
);


CREATE TABLE IF NOT EXISTS pokemon_species (
    pokemon_id INTEGER,
    species_id INTEGER,
    PRIMARY KEY (pokemon_id, species_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (species_id) REFERENCES species(species_id)
);


CREATE TABLE IF NOT EXISTS species_egg_groups (
    species_id INTEGER,
    egg_group_id INTEGER,
    PRIMARY KEY (species_id, egg_group_id),
    FOREIGN KEY (species_id) REFERENCES species(species_id),
    FOREIGN KEY (egg_group_id) REFERENCES egg_groups(egg_group_id)
);


CREATE TABLE IF NOT EXISTS pokemon_moves (
    pokemon_id INTEGER,
    move_id INTEGER,
    move_learn_method_id INTEGER,
    version_group_id INTEGER,
    level_learned_at INTEGER,
    PRIMARY KEY (pokemon_id, move_id, move_learn_method_id, version_group_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (move_id) REFERENCES moves(move_id),
    FOREIGN KEY (move_learn_method_id) REFERENCES move_learn_methods(move_learn_method_id),
    FOREIGN KEY (version_group_id) REFERENCES version_groups(version_group_id)
);


CREATE TABLE IF NOT EXISTS pokemon_encounters (
    pokemon_id INTEGER,
    version_id INTEGER,
    location_area_id INTEGER,
    encounter_method_id INTEGER,
    min_level INTEGER,
    max_level INTEGER,
    PRIMARY KEY (pokemon_id, version_id, location_area_id, encounter_method_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (version_id) REFERENCES versions(version_id),
    FOREIGN KEY (location_area_id) REFERENCES location_areas(location_area_id),
    FOREIGN KEY (encounter_method_id) REFERENCES encounter_methods(encounter_method_id)
);

CREATE TABLE IF NOT EXISTS pokemon_stats (
    pokemon_id INTEGER,
    stat_id INTEGER,
    value INTEGER,
    PRIMARY KEY (pokemon_id, stat_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (stat_id) REFERENCES stats(stat_id)
);

CREATE TABLE IF NOT EXISTS move_types (
    move_id INTEGER,
    type_id INTEGER,
    PRIMARY KEY (move_id, type_id),
    FOREIGN KEY (move_id) REFERENCES moves(move_id),
    FOREIGN KEY (type_id) REFERENCES type(type_id)
);
