using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class RootController : MonoBehaviour
{

    public GameObject gearPrefab;
    public TMP_InputField gearsIPF;
    public TMP_InputField radiusIPF;
    
    private int gears;
    private int firstRadius;
    private int rate;
    private bool runnning = false;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (this.runnning) {
            this.GetComponent<Transform>().GetChild(1).SendMessage("move", Mathf.Deg2Rad * this.rate * this.firstRadius * Time.deltaTime);
        }
    }

    public void setRate(int val) {
        this.rate = val;
    }

    public void startSim() {
        this.runnning = true;
        this.gears = int.Parse(this.gearsIPF.text);
        this.firstRadius = int.Parse(this.radiusIPF.text);
        GameObject gear = GameObject.Instantiate(this.gearPrefab);
        gear.GetComponent<Transform>().SetParent(this.GetComponent<Transform>());
        gear.SendMessage("setup", new Vector2(this.firstRadius, this.gears-1));
    }
}
