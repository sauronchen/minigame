using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public Vector3 initVel = new Vector3(0, 0, 0);
    public float maxSpeed = 20;
    public float RollForce = 10;
    public float RotationSpeed = 0.01f;
    public bool  IsRotateAsVel = true;
    //public float PitchForce = 100;
    //public float YewForce = 100;
       
    //public float g = 9.8f;        // G = mg

    public float horizonTurnThreshold_M = 5;    //angle 
    public float verticalTurnThreshold_N = 5;  //screen pixels 

    private float m = 0;   
    private float G;
    private Vector3 velocity;
    private Vector2 ScreenCenter;
    private Rigidbody rigidBody;
    private List<Vector2> touchPos;
    private Vector2[] defaultTouchPos;
    private Quaternion initRotation;

    private Transform Head;
    private Transform LeftAirfoil;
    private Transform RightAirfoil;
    private Transform Tail;
    private bool NeedSwap = false;

    // Use this for initialization
    void Start ()
    {
        velocity = initVel;
        rigidBody = GetComponent<Rigidbody>();
        rigidBody.velocity = velocity;

        m = rigidBody.mass;
        //G = m * g;

        ScreenCenter = new Vector2( Screen.width/2,Screen.height/2 );
        touchPos = new List<Vector2>();
        touchPos.Add(Vector2.zero);
        touchPos.Add(Vector2.zero);
        defaultTouchPos = new Vector2[2];
        defaultTouchPos[0] = ScreenCenter + new Vector2(100, 0);
        defaultTouchPos[1] = ScreenCenter + new Vector2(-100, 0);
        initRotation = transform.rotation;

        Head = transform.Find("Head");
        LeftAirfoil = transform.Find("LeftAirfoil");
        RightAirfoil = transform.Find("RightAirfoil");
        Tail = transform.Find("Tail");
    }


    void GetTouch()
    {
        if(Input.touchCount == 2)
        {
            touchPos[0] = Input.touches[0].position;
            touchPos[1] = Input.touches[1].position;
 //           Debug.Log( string.Format( "touch2  : {0},  {1}", touchPos[0].ToString(), touchPos[1].ToString()));
            if (Input.touches[0].phase == TouchPhase.Began || Input.touches[1].phase == TouchPhase.Began )
            {
                NeedSwap = false;
                //Debug.Log(string.Format("touchBegin  : "));
                if (touchPos[0].x > touchPos[1].x)
                {
                    //Debug.Log(string.Format("touchBeginSwap  : "));
                    NeedSwap = true;
                }
            }
            if (NeedSwap)
                touchPos.Reverse();
        }
        else
        {
            touchPos[0] = defaultTouchPos[0];
            touchPos[1] = defaultTouchPos[1];
        }
    }

    Quaternion CalRotation()
    {
        Vector2 vector = touchPos[0] - touchPos[1];
        float angleY = Mathf.Rad2Deg*Mathf.Atan( Mathf.Abs( vector.y/vector.x));
        if( Mathf.Approximately(vector.y,0f) )
        {
            angleY = 0;
        }
        else if( vector.y > 0 )
        {
            if (vector.x > 0)
                angleY = 90;
            else
                angleY = angleY;
        }
        else if(  vector.y < 0 )
        {
            if (vector.x > 0)
                angleY = -90;
            else
                angleY = -angleY;
        }
        if (Mathf.Abs(angleY) < verticalTurnThreshold_N)
            angleY = 0;


        Vector2 midPoint = (touchPos[0] + touchPos[1]) / 2f;
        float dist = midPoint.y - ScreenCenter.y;
        float angleX = 0;
        if( Mathf.Abs(dist) > verticalTurnThreshold_N )
        {
            angleX = dist / ScreenCenter.y * -90f;
        }
        return Quaternion.Euler(angleX, angleY, 0);
    }

    void AddForce( Quaternion rotation)
    {
        velocity = rigidBody.velocity;
        if (velocity.magnitude > maxSpeed)
            rigidBody.velocity = velocity = velocity.normalized * maxSpeed;

        Matrix4x4 rotateTransform = Matrix4x4.identity;
        rotateTransform.SetTRS(Vector3.zero, rotation , Vector3.one);

        Vector3 pushDir = rotateTransform * transform.forward ;
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
            Quaternion newRotation = Quaternion.Slerp(curRotation, targetRotation, Time.deltaTime);
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
