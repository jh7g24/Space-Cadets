using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RootController : MonoBehaviour
{

    public GameObject gearPrefab;
    public int gears;
    public int firstRadius;
    public int rate;

    // Start is called before the first frame update
    void Start()
    {
        GameObject gear = GameObject.Instantiate(this.gearPrefab);
        gear.GetComponent<Transform>().SetParent(this.GetComponent<Transform>());
        gear.SendMessage("setup", new Vector2(this.firstRadius, this.gears-1));
    }

    // Update is called once per frame
    void Update()
    {
        this.GetComponent<Transform>().GetChild(1).SendMessage("move", Mathf.Deg2Rad * this.rate * this.firstRadius * Time.deltaTime);
    }
}
