from main import app, db


class Album(db.Model):
    __tablename__ = 'Album'

    AlbumId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Unicode(160), nullable=False)
    ArtistId = db.Column(db.ForeignKey('Artist.ArtistId'),
                         nullable=False, index=True)

    Artist = db.relationship(
        'Artist', primaryjoin='Album.ArtistId == Artist.ArtistId', backref='albums')


class Artist(db.Model):
    __tablename__ = 'Artist'

    ArtistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Unicode(120))


class Customer(db.Model):
    __tablename__ = 'Customer'

    CustomerId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.Unicode(40), nullable=False)
    LastName = db.Column(db.Unicode(20), nullable=False)
    Company = db.Column(db.Unicode(80))
    Address = db.Column(db.Unicode(70))
    City = db.Column(db.Unicode(40))
    State = db.Column(db.Unicode(40))
    Country = db.Column(db.Unicode(40))
    PostalCode = db.Column(db.Unicode(10))
    Phone = db.Column(db.Unicode(24))
    Fax = db.Column(db.Unicode(24))
    Email = db.Column(db.Unicode(60), nullable=False)
    SupportRepId = db.Column(db.ForeignKey('Employee.EmployeeId'), index=True)

    Employee = db.relationship(
        'Employee', primaryjoin='Customer.SupportRepId == Employee.EmployeeId', backref='customers')


class Employee(db.Model):
    __tablename__ = 'Employee'

    EmployeeId = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.Unicode(20), nullable=False)
    FirstName = db.Column(db.Unicode(20), nullable=False)
    Title = db.Column(db.Unicode(30))
    ReportsTo = db.Column(db.ForeignKey('Employee.EmployeeId'), index=True)
    BirthDate = db.Column(db.DateTime)
    HireDate = db.Column(db.DateTime)
    Address = db.Column(db.Unicode(70))
    City = db.Column(db.Unicode(40))
    State = db.Column(db.Unicode(40))
    Country = db.Column(db.Unicode(40))
    PostalCode = db.Column(db.Unicode(10))
    Phone = db.Column(db.Unicode(24))
    Fax = db.Column(db.Unicode(24))
    Email = db.Column(db.Unicode(60))

    parent = db.relationship('Employee', remote_side=[
                             EmployeeId], primaryjoin='Employee.ReportsTo == Employee.EmployeeId', backref='employees')


class Genre(db.Model):
    __tablename__ = 'Genre'

    GenreId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Unicode(120))


class Invoice(db.Model):
    __tablename__ = 'Invoice'

    InvoiceId = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.ForeignKey(
        'Customer.CustomerId'), nullable=False, index=True)
    InvoiceDate = db.Column(db.DateTime, nullable=False)
    BillingAddress = db.Column(db.Unicode(70))
    BillingCity = db.Column(db.Unicode(40))
    BillingState = db.Column(db.Unicode(40))
    BillingCountry = db.Column(db.Unicode(40))
    BillingPostalCode = db.Column(db.Unicode(10))
    Total = db.Column(db.Numeric(10, 2), nullable=False)

    Customer = db.relationship(
        'Customer', primaryjoin='Invoice.CustomerId == Customer.CustomerId', backref='invoices')


class InvoiceLine(db.Model):
    __tablename__ = 'InvoiceLine'

    InvoiceLineId = db.Column(db.Integer, primary_key=True)
    InvoiceId = db.Column(db.ForeignKey(
        'Invoice.InvoiceId'), nullable=False, index=True)
    TrackId = db.Column(db.ForeignKey('Track.TrackId'),
                        nullable=False, index=True)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

    Invoice = db.relationship(
        'Invoice', primaryjoin='InvoiceLine.InvoiceId == Invoice.InvoiceId', backref='invoice_lines')
    Track = db.relationship(
        'Track', primaryjoin='InvoiceLine.TrackId == Track.TrackId', backref='invoice_lines')


class MediaType(db.Model):
    __tablename__ = 'MediaType'

    MediaTypeId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Unicode(120))


class Playlist(db.Model):
    __tablename__ = 'Playlist'

    PlaylistId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Unicode(120))

    Track = db.relationship(
        'Track', secondary='PlaylistTrack', backref='playlists')


t_PlaylistTrack = db.Table(
    'PlaylistTrack',
    db.Column('PlaylistId', db.ForeignKey('Playlist.PlaylistId'),
              primary_key=True, nullable=False),
    db.Column('TrackId', db.ForeignKey('Track.TrackId'),
              primary_key=True, nullable=False, index=True)
)


class Track(db.Model):
    __tablename__ = 'Track'

    TrackId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Unicode(200), nullable=False)
    AlbumId = db.Column(db.ForeignKey('Album.AlbumId'), index=True)
    MediaTypeId = db.Column(db.ForeignKey(
        'MediaType.MediaTypeId'), nullable=False, index=True)
    GenreId = db.Column(db.ForeignKey('Genre.GenreId'), index=True)
    Composer = db.Column(db.Unicode(220))
    Milliseconds = db.Column(db.Integer, nullable=False)
    Bytes = db.Column(db.Integer)
    UnitPrice = db.Column(db.Numeric(10, 2), nullable=False)

    Album = db.relationship(
        'Album', primaryjoin='Track.AlbumId == Album.AlbumId', backref='tracks')
    Genre = db.relationship(
        'Genre', primaryjoin='Track.GenreId == Genre.GenreId', backref='tracks')
    MediaType = db.relationship(
        'MediaType', primaryjoin='Track.MediaTypeId == MediaType.MediaTypeId', backref='tracks')


# create db if not exists
with app.app_context():
    db.create_all()
