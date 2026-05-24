package ooap.datastructures.Java_cli_5;

public class Unit {
    protected String name;

    public Unit(String name) {
        this.name = name;
    }

    public void printName() {
        System.out.println("class Unit " + this.name);
    }
}