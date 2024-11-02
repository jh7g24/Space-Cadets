using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GearController : MonoBehaviour
{
    
    public GameObject gearPrefab;
    public GameObject inkPrefab;
    public bool penOn = false;

    private GameObject inkContainer;
    private int radius;
    private int depth;
    


    // r is radius to be set
    void setup(Vector2 args) {
        this.inkContainer = GameObject.Find("Ink Blobs");
        this.radius = (int) args[0];
        this.GetComponent<Transform>().position = this.GetComponent<Transform>().parent.position + new Vector3(this.radius, 0, 0);
        if (args[1] > 0) {
            GameObject gear = GameObject.Instantiate(gearPrefab);
            gear.GetComponent<Transform>().SetParent(this.GetComponent<Transform>());
            gear.SendMessage("setup", new Vector2(this.radius * 0.25f, args[1]-1));
        } else {
            this.penDown();
        }
    }

    public void move(float arcLength) {
        float angle = Mathf.Rad2Deg * (arcLength / this.radius);
        this.GetComponent<Transform>().RotateAround(this.GetComponent<Transform>().parent.position, this.GetComponent<Transform>().up, angle);
        if (this.GetComponent<Transform>().childCount == 2) {
            this.GetComponent<Transform>().GetChild(1).SendMessage("move", Mathf.Deg2Rad * angle * this.radius);
        }
        if (this.penOn) {
            GameObject inkBlob = GameObject.Instantiate(this.inkPrefab);
            inkBlob.GetComponent<Transform>().position = this.GetComponent<Transform>().position;
            inkBlob.GetComponent<Transform>().parent = this.inkContainer.GetComponent<Transform>();
        }
    }

    public void penUp() {
        this.penOn = false;
    }

    public void penDown() {
        this.penOn = true;
    }
}
