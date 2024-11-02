using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InkController : MonoBehaviour
{
    public Material mat;

    private Color red = new Color(255, 0, 0);
    private Color blue = new Color(0, 0, 255);
    private Color green = new Color(0, 255, 0);


    public void setInkRed() {
        this.mat.color = this.red;
    }

    public void setInkBlue() {
        this.mat.color = this.blue;
    }

    public void setInkGreen() {
        this.mat.color = this.green;
    }

    public void setInkTransparent(){}
    public void setInk(){}
}
