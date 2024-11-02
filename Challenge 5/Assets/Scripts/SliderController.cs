using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class SliderController : MonoBehaviour
{

    public TMP_Text text;
    public GameObject root;

    // Start is called before the first frame update
    void Start()
    {
        this.updateText();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void incr() {
        this.GetComponent<Slider>().value++;
    }

    public void decr() {
        this.GetComponent<Slider>().value--;
    }

    public void updateText() {
        this.text.text = this.GetComponent<Slider>().value.ToString();
        this.root.SendMessage("setRate", this.GetComponent<Slider>().value);
    }
}
