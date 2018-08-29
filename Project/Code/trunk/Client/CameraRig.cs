using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRig : MonoBehaviour
{
    public float smoothTime = 0;
    public Vector3 dist = Vector3.one;
    public GameObject target;
    public Vector3 moveVel = Vector3.zero;


    private Transform rigTransform;

    // Use this for initialization
    void Start ()
    {
        rigTransform = this.transform;
    }


    void FixedUpdate()
    {

    }


    // Update is called once per frame
    void Update ()
    {
		if (target == null)
        {
            return;
        }
        rigTransform.position = Vector3.SmoothDamp(rigTransform.position, target.transform.position + dist, ref moveVel, smoothTime);
	}


    void OnCollisionEnter(Collision col)
    {
        col.collider.gameObject.GetComponent<Transform>();

    }
}
