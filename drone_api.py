from firebase_config import db
from fastapi import HTTPException

DRONE_COLLECTION = "drones"


# ----------------------------
# FETCH SINGLE DRONE
# ----------------------------
def get_drone(drone_id: str):
    doc = db.collection(DRONE_COLLECTION).document(drone_id).get()
    if not doc.exists:
        raise HTTPException(
            status_code=404,
            detail=f"Drone '{drone_id}' not found"
        )
    return doc.to_dict()


# ----------------------------
# DEPLOY DRONE
# ----------------------------
def deploy_drone(drone_id: str, mission: str):
    drone = get_drone(drone_id)

    status = drone.get("status")
    battery = drone.get("battery")

    # Battery guardrail
    if battery < 20:
        raise HTTPException(
            status_code=400,
            detail=f"{drone_id} battery too low ({battery}%)"
        )

    # Status validation
    if status not in ["Idle", "Charging", "offline"]:
        raise HTTPException(
            status_code=400,
            detail=f"{drone_id} not available (Status: {status})"
        )

    # Update drone
    db.collection(DRONE_COLLECTION).document(drone_id).update({
        "status": "In-Flight",
        "mission": mission
    })

    return {"message": f"{drone_id} deployed for mission '{mission}'"}


# ----------------------------
# DRONE RETURNING TO BASE
# ----------------------------
def recover_drone(drone_id: str):
    get_drone(drone_id)

    db.collection(DRONE_COLLECTION).document(drone_id).update({
        "status": "Returning",
        "mission": "RTB"
    })

    return {"message": f"{drone_id} returning to base"}


# ----------------------------
# FULLY CHARGE DRONE
# ----------------------------
def charge_drone(drone_id: str):
    get_drone(drone_id)

    db.collection(DRONE_COLLECTION).document(drone_id).update({
        "battery": 100,
        "status": "Charging"
    })

    return {"message": f"{drone_id} fully charged"}
