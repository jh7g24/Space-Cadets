using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MarkerController : MonoBehaviour
{
    
    public void toggleMarker() {
        this.GetComponent<MeshRenderer>().enabled = !this.GetComponent<MeshRenderer>().enabled;
    }
}
