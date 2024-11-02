using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class DropDownController : MonoBehaviour
{

    public GameObject inkContainer;

    void Start() {
        Debug.Log("now");
        this.changeColors();
    }

    public void changeColors() {
        string color;
        switch (this.GetComponent<TMP_Dropdown>().value) {
            case 0:
                color = "Red";
                break;
            case 1:
                color = "Green";
                break;
            case 2:
                color = "Blue";
                break;
            case 3:
                color = "Transparent";
                break;
            default:
                color="";
                break;
        }
        if (color == "Transparent") {
            this.inkContainer.SetActive(false);
        } else {
            this.inkContainer.SetActive(true);
        }
        string func = "setInk" + color;
        this.inkContainer.BroadcastMessage(func);
    }
}
