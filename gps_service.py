class GPSSignalLostError(Exception):
    """Ngoai le tuy chinh khi thiet bi mat tin hieu dinh vi GPS."""
    pass

def get_current_location():
    """Ham mo phong truy cap phan cung GPS dien thoai de lay toa do."""
    return (10.0, 105.0)