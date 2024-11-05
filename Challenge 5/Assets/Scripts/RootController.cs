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
    public TMP_InputField radiusRatiosIPF;
    
    private int gears;
    private float firstRadius;
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
        this.firstRadius = float.Parse(this.radiusIPF.text);


        GameObject gear = GameObject.Instantiate(this.gearPrefab);
        gear.GetComponent<Transform>().SetParent(this.GetComponent<Transform>());

        float[] ratios = this.unpackRatios(this.radiusRatiosIPF.text);
        gearsData setupParams = new gearsData(this.firstRadius, this.gears-1, ratios);
        gear.SendMessage("setup", setupParams);
    }

    private float[] unpackRatios(string inputString) {
        string[] ratiosSTR = inputString.Split(',');
        float[] ratios = new float[this.gears];
        for (int i = 0; i < ratiosSTR.Length; i++) {
            ratios[i] = float.Parse(ratiosSTR[i]);
        }
        while (ratios.Length < this.gears) {
            ratios[ratios.Length] = ratios[ratios.Length - 1];
        }
        this.printArray(ratios);
        return ratios;
    }

    private void printArray(float[] arr) {
        foreach (float item in arr) {
            Debug.Log(item);
        }
    }
}

public struct gearsData {
    public float radius;
    public int depth;
    public float[] ratios;

    public gearsData(float r, int d, float[] rs) {
        this.radius = r;
        this.depth = d;
        this.ratios = rs;
    }
}

