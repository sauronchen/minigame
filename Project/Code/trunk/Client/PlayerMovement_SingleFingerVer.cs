using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement_SingleFingerVer: MonoBehaviour
{
    public Vector3 initVel = new Vector3(0, 0, 0);
    public float maxSpeed = 20;
    public float RollForce = 10;
    public float RotationSpeed = 0.5f;
    public bool  IsRotateAsVel = false;

    public float XMaxDist = 400;   
    public float YMaxDist = 300;  

    private float m = 0;   
    private Vector2 touchPos;
    private Vector2 dirVec;
    private Vector3 velocity;
    private Vector3 iniForward;
    private Rigidbody rigidBody;
    private Quaternion initRotation;

    // Use this for initialization
    void Start ()
    {
        velocity = initVel;
        iniForward = this.gameObject.transform.forward;
        rigidBody = GetComponent<Rigidbody>();
        rigidBody.velocity = velocity;

        m = rigidBody.mass;

        touchPos = Vector2.zero;
        initRotation = transform.rotation;
    }


    void GetTouch()
    {
        if(Input.touchCount == 1)
        {
            if ( Input.touches[0].phase == TouchPhase.Began )
            {
                touchPos = Input.touches[0].position;
            }
            dirVec = Input.touches[0].position - touchPos;
        }
    }

    Quaternion CalRotation()
    {
        Vector2 vector = dirVec;
        if (Mathf.Approximately(vector.x, 0f) && Mathf.Approximately(vector.y, 0f))
            return Quaternion.identity;

        float angleX = Mathf.Clamp( vector.y / YMaxDist ,-1f, 1f )* -90f;
        float angleY = Mathf.Clamp( vector.x / XMaxDist ,-1f, 1f )* 90f;

        return Quaternion.Euler(angleX, angleY, 0);
    }

    void AddForce( Quaternion rotation)
    {
        velocity = rigidBody.velocity;
        if (velocity.magnitude > maxSpeed)
            rigidBody.velocity = velocity = velocity.normalized * maxSpeed;

        Matrix4x4 rotateTransform = Matrix4x4.identity;
        rotateTransform.SetTRS(Vector3.zero, rotation , Vector3.one);

        Vector3 pushDir = rotateTransform * iniForward ;
        pushDir.Normalize();
        rigidBody.AddForce(pushDir*RollForce);

        if( IsRotateAsVel )
        {
            Quaternion DstRotation = Quaternion.FromToRotation(Vector3.forward, velocity);
            transform.rotation = DstRotation;
        }
        else
        {
            Quaternion curRotation = transform.rotation;
            Quaternion targetRotation = initRotation * rotation;
            Quaternion newRotation = Quaternion.Slerp(curRotation, targetRotation, RotationSpeed);
            transform.rotation = newRotation;
        }


        //       Debug.Log(velocity.z);
        //  transform.Translate(velocity * Time.deltaTime);


        /*
        //俯冲
        if (Input.GetKey(KeyCode.W))
        {
            rigidBody.AddForceAtPosition(transform.up * -PitchForce, Head.position);

            rigidBody.AddForceAtPosition(transform.up * PitchForce, Tail.position);
        }
        //爬升
        else if (Input.GetKey(KeyCode.S))
        {
            rigidBody.AddForceAtPosition(transform.up * PitchForce, Head.position);

            rigidBody.AddForceAtPosition(transform.up * -PitchForce, Tail.position);
        }
        //左翻滚
        else if (Input.GetKey(KeyCode.A))
        {
            rigidBody.AddForceAtPosition(transform.up * -RollForce, LeftAirfoil.position);

            rigidBody.AddForceAtPosition(transform.up * RollForce, RightAirfoil.position);
        }
        //右翻滚
        else if (Input.GetKey(KeyCode.D))
        {
            rigidBody.AddForceAtPosition(transform.up * RollForce, LeftAirfoil.position);

            rigidBody.AddForceAtPosition(transform.up * -RollForce, RightAirfoil.position);
        }
        //左转
        else if(Input.GetKey(KeyCode.Q))
        {
            rigidBody.AddForceAtPosition(transform.right * -YewForce, Head.position);

            rigidBody.AddForceAtPosition(transform.right * YewForce, Tail.position);
        }
        //右转
        else if (Input.GetKey(KeyCode.E))
        {
            rigidBody.AddForceAtPosition(transform.right * YewForce, Head.position);

            rigidBody.AddForceAtPosition(transform.right * -YewForce, Tail.position);
        }
        */

    }


    void FixedUpdate()
    {
        GetTouch();
        Quaternion rotation = CalRotation();
        AddForce(rotation);
    }



    // Update is called once per frame
    void Update () {
		
	}

    void OnCollisionEnter()
    {

    }
}
