from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import bcrypt
import logging

logger = logging.getLogger(__name__)

# Try to initialize passlib, but use bcrypt directly if it fails
pwd_context = None
USE_PASSLIB = False

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Test if passlib works by trying to hash a test password
    try:
        test_hash = pwd_context.hash("test")
        USE_PASSLIB = True
        logger.info("Using passlib for password hashing")
    except Exception as e:
        logger.warning(f"passlib initialization failed, using bcrypt directly: {e}")
        USE_PASSLIB = False
        pwd_context = None
except Exception as e:
    logger.warning(f"passlib context creation failed, using bcrypt directly: {e}")
    USE_PASSLIB = False
    pwd_context = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    import logging
    logger = logging.getLogger(__name__)
    
    # Truncate password to 72 bytes if necessary (same as in get_password_hash)
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        logger.warning(f"Password for verification exceeds 72 bytes ({len(password_bytes)} bytes), truncating...")
        # Truncate to exactly 72 bytes
        password_bytes = password_bytes[:72]
        
        # Decode back to string, handling incomplete UTF-8 sequences
        decoded_password = None
        temp_bytes = password_bytes
        attempts = 0
        while len(temp_bytes) > 0 and attempts < 10:
            try:
                decoded_password = temp_bytes.decode('utf-8')
                break
            except UnicodeDecodeError:
                temp_bytes = temp_bytes[:-1]
                attempts += 1
        
        if decoded_password is not None:
            plain_password = decoded_password
        else:
            # Fallback: truncate by characters
            plain_password = plain_password[:50]
            while len(plain_password.encode('utf-8')) > 72 and len(plain_password) > 0:
                plain_password = plain_password[:-1]
        
        # Final check
        final_check = plain_password.encode('utf-8')
        if len(final_check) > 72:
            final_check = final_check[:72]
            try:
                plain_password = final_check.decode('utf-8', errors='ignore')
            except:
                plain_password = plain_password[:25]
    
    # Verify the password
    # Always use bcrypt directly since passlib is having issues
    # Both passlib and direct bcrypt create compatible hashes
    try:
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        result = bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        logger.debug(f"Password verification result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error with bcrypt verification: {e}")
        # Try with passlib as fallback if available
        if USE_PASSLIB:
            try:
                return pwd_context.verify(plain_password, hashed_password)
            except Exception as e2:
                logger.error(f"Error with passlib verification: {e2}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password - bcrypt has a strict 72 byte limit"""
    import logging
    logger = logging.getLogger(__name__)
    
    # Convert to bytes immediately to check length
    password_bytes = password.encode('utf-8')
    original_byte_length = len(password_bytes)
    
    # Log original length
    logger.info(f"Password received: {original_byte_length} bytes")
    
    # ALWAYS ensure password is <= 72 bytes before hashing
    # Use a simple, foolproof approach: truncate bytes and decode safely
    if original_byte_length > 72:
        logger.warning(f"Password exceeds 72 bytes ({original_byte_length} bytes), truncating...")
        # Truncate to exactly 72 bytes
        password_bytes = password_bytes[:72]
        
        # Decode back to string, handling incomplete UTF-8 sequences
        # Remove trailing bytes until we get valid UTF-8
        decoded_password = None
        temp_bytes = password_bytes
        max_attempts = 10
        attempts = 0
        
        while len(temp_bytes) > 0 and attempts < max_attempts:
            try:
                decoded_password = temp_bytes.decode('utf-8')
                break
            except UnicodeDecodeError:
                # Remove last byte and try again
                temp_bytes = temp_bytes[:-1]
                attempts += 1
        
        # Use decoded password if successful
        if decoded_password is not None:
            password = decoded_password
            # Verify the decoded password is <= 72 bytes
            check_bytes = password.encode('utf-8')
            if len(check_bytes) > 72:
                # If still too long (shouldn't happen), truncate more aggressively
                logger.error(f"Decoded password still {len(check_bytes)} bytes, truncating further...")
                while len(password.encode('utf-8')) > 72 and len(password) > 0:
                    password = password[:-1]
        else:
            # Fallback: truncate original password by characters
            logger.error("Failed to decode truncated password, using character truncation")
            original_password = password  # Keep reference to original
            password = original_password[:50]  # Start with safe truncation
            # Keep truncating until bytes <= 72
            while len(password.encode('utf-8')) > 72 and len(password) > 0:
                password = password[:-1]
    
    # ABSOLUTE FINAL CHECK: ensure password is <= 72 bytes
    final_check = password.encode('utf-8')
    final_length = len(final_check)
    
    if final_length > 72:
        logger.error(f"CRITICAL ERROR: Password still {final_length} bytes after all truncation attempts!")
        # Emergency: truncate byte-by-byte
        final_check = final_check[:72]
        # Try to decode
        try:
            password = final_check.decode('utf-8', errors='ignore')
        except:
            # Last resort: use first 30 characters
            password = password[:30]
        final_length = len(password.encode('utf-8'))
        logger.warning(f"Emergency truncation applied, final length: {final_length} bytes")
    
    # ONE MORE ABSOLUTE CHECK
    absolute_final = password.encode('utf-8')
    if len(absolute_final) > 72:
        logger.error(f"FATAL: Password STILL too long ({len(absolute_final)} bytes)! Using extreme truncation!")
        password = password[:25]  # Extreme fallback
    
    final_byte_length = len(password.encode('utf-8'))
    logger.info(f"Hashing password with final length: {final_byte_length} bytes")
    
    # Hash the password (guaranteed to be <= 72 bytes)
    # Use bcrypt directly since passlib is having issues
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        logger.info("Password hashed successfully with direct bcrypt")
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password with bcrypt: {e}")
        # Try passlib as fallback if available
        if USE_PASSLIB and pwd_context:
            try:
                result = pwd_context.hash(password)
                logger.info("Password hashed successfully with passlib (fallback)")
                return result
            except Exception as e2:
                logger.error(f"Error with passlib fallback: {e2}")
        raise


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

