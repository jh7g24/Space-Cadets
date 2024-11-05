using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraController : MonoBehaviour
{
    public Slider zoomSlider;

    private int minZoomY = 5;
    private int maxZoomY = 500;

    public void changeZoom() {
        this.GetComponent<Transform>().position = new Vector3(0, Mathf.Lerp( this.maxZoomY, this.minZoomY, this.zoomSlider.value), 0);
    }
}
