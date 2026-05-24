package ooap.datastructures.Java_cli_5;

import ooap.datastructures.Java_cli_5.Unit;


public class SwordsMan extends Unit {

    public SwordsMan() {
        super("swordsman");
    }

    public void attack(int damage) {
        System.out.println("Attack with sword. Damage: " + damage);
    }

    public void attack(int damage, int bonus) {
        System.out.println("Attack with bonus. Damage: " + (damage + bonus));
    }

    public void attack(String target) {
        System.out.println("Attack target: " + target);
    }
}
